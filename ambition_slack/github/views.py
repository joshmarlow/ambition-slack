import json
import logging
import os

from django.http import HttpResponse
from django.views.generic.base import View
from manager_utils import get_or_none
import slack
import slack.chat
import slack.users

from ambition_slack.github.models import GithubUser


slack.api_token = os.environ['SLACK_API_TOKEN']
LOG = logging.getLogger('console_logger')


class GithubPayload(object):
    """
    This class provides a wrapper around the Github API posts.
    """
    def __init__(self, message_dict):
        self.message_dict = message_dict

    @property
    def action(self):
        return self.message_dict['action']

    @property
    def assignee_login(self):
        try:
            return self.message_dict['pull_request']['assignee'].get('login')
        except (IndexError, AttributeError):
            return None

    @property
    def sender_login(self):
        try:
            return self.message_dict['sender']['login']
        except IndexError:
            return None

    @property
    def is_pull_request_action(self):
        return self.is_repo_action and self.is_pull_request

    @property
    def is_pull_request_comment(self):
        return self.is_issue and self.action == 'created'

    @property
    def is_closed(self):
        return self.action == 'closed'

    @property
    def is_assigned(self):
        return self.action == 'assigned'

    @property
    def is_opened_or_merged(self):
        return self.action in ['opened', 'closed', 'merged']

    @property
    def is_repo_action(self):
        return self.is_opened_or_merged or self.is_assigned or self.is_closed

    @property
    def is_issue(self):
        return 'issue' in self.message_dict

    @property
    def is_pull_request(self):
        return 'pull_request' in self.message_dict

    @property
    def new_pull_request_comment(self):
        return self.is_issue and self.is_created_action

    @property
    def pull_request_html_url(self):
        try:
            return self.message_dict['pull_request']['html_url']
        except IndexError:
            return None

    @property
    def pull_request_comment(self):
        try:
            return self.message_dict['issue']['pull_request']['html_url']
        except IndexError:
            return None

    @property
    def pull_request_body(self):
        try:
            return self.message_dict['pull_request']['body']
        except IndexError:
            return None

    @property
    def comment_body(self):
        return self.message_dict['comment']['body']


class GithubView(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Github')

    def handle_pull_request_repo_action(self, payload):
        """
        Handles a new pull request action on a repo (open, close, merge, assign) and notifies the proper slack user.
        """
        # Find out who made the action and who was assigned
        sender = GithubUser.objects.get(username__iexact=payload.sender_login)
        assignee = get_or_none(GithubUser.objects, username__iexact=payload.assignee_login)

        if payload.is_opened_or_merged or payload.is_closed:
            # In this case, a PR was opened, reopened, closed or merged
            github_users = GithubUser.objects.select_related('slack_user')
            for gh_user in github_users:
                if '@{}'.format(gh_user.username) in payload.pull_request_body.lower() or assignee == gh_user:
                    slack.chat.post_message(
                        '@{}'.format(gh_user.slack_user.username),
                        'Pull request {} by {} - ({})'.format(
                            payload.action, sender.slack_user.name, payload.pull_request_html_url),
                        username='github')
        elif payload.is_assigned:
            # In this case, a new person was assigned to the PR
            slack.chat.post_message(
                '@{}'.format(assignee.slack_user.username),
                'Pull request {} to you by {} - ({})'.format(
                    payload.action, sender.slack_user.name, payload.pull_request_html_url),
                username='github')

    def handle_pull_request_comment_action(self, payload):
        """
        Handles a comment on a pull request and notifies the proper slack user if they were tagged.
        """
        sender = GithubUser.objects.get(username__iexact=payload.sender_login)

        # In this case, a comment was created on the PR. Notify anyone tagged.
        github_users = GithubUser.objects.select_related('slack_user')
        for gh_user in github_users:
            if '@{}'.format(gh_user.username) in payload.comment_body.lower():
                slack.chat.post_message(
                    '@{}'.format(gh_user.slack_user.username),
                    'Pull request comment from {} - ({})'.format(
                        sender.slack_user.name, payload.pull_request_comment),
                    username='github')

    def post(self, request, *args, **kwargs):
        """
        Handles webhook posts from Github
        """
        payload = GithubPayload(json.loads(request.body))

        if payload.is_pull_request_action:
            self.handle_pull_request_repo_action(payload)
        elif payload.is_pull_request_comment:
            self.handle_pull_request_comment_action(payload)

        return HttpResponse()
