import logging

import slack
import slack.chat
import slack.users

from ambition_slack.slack.models import SlackUser


LOG = logging.getLogger(__name__)


class MorningDigest(object):
    """
    This class handles constructing and sending a morning digest customized for each developer.
    """
    def __init__(self, slack_user):
        self.slack_user = slack_user

    @property
    def channel_name(self):
        return '@{0}'.format(self.slack_user.username)

    @property
    def message(self):
        return {
            'username': 'Digest',
        }

    def _construct_attachments(self):
        """
        Construct the actual digest content.
        """
        attachments = []

        # Add reminder to post scrum in #engineering
        attachments.append({
            'text': 'Remember to post Standup in #engineering',
        })

        # TODO: Add reminder about pending pull requests

        # TODO: Add reminder about any all day events

        return attachments

    def post_to_slack(self):
        """
        Post the digest to slack.
        """
        if not self.slack_user:
            LOG.error('post_to_slack called when slack_user = None')
            return

        # TODO: if the user is out of the office (check calendar) then don't post anything for them

        slack.chat.post_message(
            self.channel_name, self.message, attachments=self._construct_attachments())


def send_digest_to_all_slack_users():
    """
    Create and post a morning digest for all slack users.
    """
    for su in SlackUser.objects.filter(username='joshmarlow'):
        MorningDigest(su).post_to_slack()
