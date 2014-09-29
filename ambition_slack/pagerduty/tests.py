
import json

from django.db import IntegrityError
from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from mock import patch, call

from ambition_slack.pagerduty.models import PagerdutyUser
from ambition_slack.slack.models import SlackUser


class PagerdutyModelsTest(TransactionTestCase):

    """
    Tests various aspects of the github models.
    """
    def test_multiple_pagerduty_per_slack_user_not_allowed(self):
        # Try to create multiple pagerduty users for the same slack user
        slack_user = SlackUser.objects.create(
            email='adam@nuhnuhnuhnuh.com', username='batman', name='Adam')
        PagerdutyUser.objects.create(slack_user=slack_user, email='adam@nuhnuhnuhnuh.com')
        with self.assertRaises(IntegrityError):
            PagerdutyUser.objects.create(slack_user=slack_user, email='joker@gothamcity.com')

    def test_github_unicode(self):
        pagerduty_user = PagerdutyUser(email='adam@nuhnuhnuhnuh.com')
        self.assertEquals(pagerduty_user.__unicode__(), 'adam@nuhnuhnuhnuh.com')


class TestPagerdutyView(TestCase):
    def setUp(self):
        self.client = Client()
        # this payload includes multiple messages ex.2 triggers and 1 resolve types
        self.example_multiple_payload = {
            'messages': [{
                'type': 'incident.trigger',
                'data': {
                    'incident': {
                        'id': 'PLKJG51',
                        'incident_number': 4177,
                        'created_on': '2014-09-26T10:02:24-04:00',
                        'status': 'triggered',
                        'html_url': 'https://ambition.pagerduty.com/incidents/PLKJG51',
                        'incident_key': '44e5fad84a8b4effad1d940ca41efadd',
                        'service': {
                            'id': 'PPIYLHG',
                            'name': 'Ambition File Processor',
                            'html_url': 'https://ambition.pagerduty.com/services/PPIYLHG',
                            'deleted_at': None},
                        'escalation_policy': {
                            'id': 'PU2XJM5',
                            'name': 'Data Uploads',
                            'deleted_at': None},
                        'assigned_to_user': {
                            'id': 'PC3L3KU',
                            'name': 'Wes Kendall',
                            'email': 'wes.kendall@ambition.com',
                            'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU'},
                        'trigger_summary_data': {
                            'subject': 'False Alarm Description Field'},
                        'trigger_details_html_url':
                            'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R',
                        'trigger_type': 'web_trigger',
                        'last_status_change_on': '2014-09-26T10:02:24-04:00',
                        'last_status_change_by': None,
                        'number_of_escalations': 0,
                        'assigned_to': [{
                            'at': '2014-09-26T10:02:24-04:00',
                            'object': {
                                'id': 'PC3L3KU',
                                'name': 'Wes Kendall',
                                'email': 'wes.kendall@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU',
                                'type': 'user'}},
                            {
                            'at': '2014-09-26T10:02:24-04:00',
                            'object': {
                                'id': 'POO8763',
                                'name': 'Josh Marlow',
                                'email': 'josh.marlow@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/POO8763',
                                'type': 'user'}},
                            {
                            'at': '2014-09-26T10:02:24-04:00',
                            'object': {
                                'id': 'P0TO520',
                                'name': 'Wayne Fullam',
                                'email': 'wayne.fullam@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/P0TO520',
                                'type': 'user'}}]}},
                        'id': 'be03bb40-4585-11e4-a431-12313f0a2181',
                        'created_on': '2014-09-26T14:02:24Z'},
                {
                'type': 'incident.resolve',
                'data': {
                    'incident': {
                        'id': 'PLKJG51',
                        'incident_number': 4177,
                        'created_on': '2014-09-26T14:02:24Z',
                        'status': 'resolved',
                        'html_url': 'https://ambition.pagerduty.com/incidents/PLKJG51',
                        'incident_key': '44e5fad84a8b4effad1d940ca41efadd',
                        'service': {
                            'id': 'PPIYLHG',
                            'name': 'Ambition File Processor',
                            'html_url': 'https://ambition.pagerduty.com/services/PPIYLHG',
                            'deleted_at': None},
                        'escalation_policy': {
                            'id': 'PU2XJM5',
                            'name': 'Data Uploads',
                            'deleted_at': None},
                        'assigned_to_user': None,
                        'trigger_summary_data': {
                            'subject': 'False Alarm Description Field'},
                        'trigger_details_html_url':
                            'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R',
                        'trigger_type': 'web_trigger',
                        'last_status_change_on': '2014-09-26T14:03:50Z',
                        'last_status_change_by': {
                            'id': 'PC3L3KU',
                            'name': 'Wes Kendall',
                            'email': 'wes.kendall@ambition.com',
                            'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU'},
                        'number_of_escalations': 0,
                        'resolved_by_user': {
                            'id': 'PC3L3KU',
                            'name': 'Wes Kendall',
                            'email': 'wes.kendall@ambition.com',
                            'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU'},
                        'assigned_to': []}},
                    'id': 'f13ab180-4585-11e4-a34d-22000ad9bf74',
                    'created_on': '2014-09-26T14:03:50Z'},
                {
                'type': 'incident.escalate',
                'data': {
                    'incident': {
                        'id': 'PL3ZU2L',
                        'incident_number': 4178,
                        'created_on': '2014-09-26T10:06:19-04:00',
                        'status': 'triggered',
                        'html_url': 'https://ambition.pagerduty.com/incidents/PL3ZU2L',
                        'incident_key': '42b6402c4f2747a592cd57815b890a17',
                        'service': {
                            'id': 'PPIYLHG',
                            'name': 'Ambition File Processor',
                            'html_url': 'https://ambition.pagerduty.com/services/PPIYLHG',
                            'deleted_at': None},
                        'escalation_policy': {
                            'id': 'PU2XJM5',
                            'name': 'Data Uploads',
                            'deleted_at': None},
                        'assigned_to_user': {
                            'id': 'PC3L3KU',
                            'name': 'Wes Kendall',
                            'email': 'wes.kendall@ambition.com',
                            'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU'},
                        'trigger_summary_data': {
                            'subject': 'False Alarm Test'},
                        'trigger_details_html_url':
                            'https://ambition.pagerduty.com/incidents/PL3ZU2L/log_entries/PJFGST7',
                        'trigger_type': 'web_trigger',
                        'last_status_change_on': '2014-09-26T10:06:19-04:00',
                        'last_status_change_by': None,
                        'number_of_escalations': 0,
                        'assigned_to': [{
                            'at': '2014-09-26T10:06:19-04:00',
                            'object': {
                                'id': 'PC3L3KU',
                                'name': 'Wes Kendall',
                                'email': 'wes.kendall@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU',
                                'type': 'user'}},
                            {
                            'at': '2014-09-26T10:06:19-04:00',
                            'object': {
                                'id': 'POO8763',
                                'name': 'Josh Marlow',
                                'email': 'josh.marlow@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/POO8763',
                                'type': 'user'}},
                            {
                            'at': '2014-09-26T10:06:19-04:00',
                            'object': {
                                'id': 'P0TO520',
                                'name': 'Wayne Fullam',
                                'email': 'wayne.fullam@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/P0TO520',
                                'type': 'user'}}]}},
                    'id': '4a66e8f0-4586-11e4-87f5-22000ae31361',
                    'created_on': '2014-09-26T14:06:19Z'}]}
        # this is an example payload for a single message, in this case type - trigger
        self.example_single_trigger_payload = {
            'messages': [{
                'type': 'incident.trigger',
                'data': {
                    'incident': {
                        'id': 'PLKJG51',
                        'incident_number': 4177,
                        'created_on': '2014-09-26T10:02:24-04:00',
                        'status': 'triggered',
                        'html_url': 'https://ambition.pagerduty.com/incidents/PLKJG51',
                        'incident_key': '44e5fad84a8b4effad1d940ca41efadd',
                        'service': {
                            'id': 'PPIYLHG',
                            'name': 'Ambition File Processor',
                            'html_url': 'https://ambition.pagerduty.com/services/PPIYLHG',
                            'deleted_at': None},
                        'escalation_policy': {
                            'id': 'PU2XJM5',
                            'name': 'Data Uploads',
                            'deleted_at': None},
                        'assigned_to_user': {
                            'id': 'PC3L3KU',
                            'name': 'Wes Kendall',
                            'email': 'wes.kendall@ambition.com',
                            'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU'},
                        'trigger_summary_data': {
                            'subject': 'False Alarm Description Field'},
                        'trigger_details_html_url':
                            'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R',
                        'trigger_type': 'web_trigger',
                        'last_status_change_on': '2014-09-26T10:02:24-04:00',
                        'last_status_change_by': None,
                        'number_of_escalations': 0,
                        'assigned_to': [{
                            'at': '2014-09-26T10:02:24-04:00',
                            'object': {
                                'id': 'PC3L3KU',
                                'name': 'Wes Kendall',
                                'email': 'wes.kendall@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU',
                                'type': 'user'}},
                            {
                            'at': '2014-09-26T10:02:24-04:00',
                            'object': {
                                'id': 'POO8763',
                                'name': 'Josh Marlow',
                                'email': 'josh.marlow@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/POO8763',
                                'type': 'user'}},
                            {
                            'at': '2014-09-26T10:02:24-04:00',
                            'object': {
                                'id': 'P0TO520',
                                'name': 'Wayne Fullam',
                                'email': 'wayne.fullam@ambition.com',
                                'html_url': 'https://ambition.pagerduty.com/users/P0TO520',
                                'type': 'user'}}]}},
                        'id': 'be03bb40-4585-11e4-a431-12313f0a2181',
                        'created_on': '2014-09-26T14:02:24Z'},
                ]}
        # this is an example payload for a single message, in this case type - resolve
        self.example_single_resolve_payload = {
            'messages': [{
                'type': 'incident.resolve',
                'data': {
                    'incident': {
                        'id': 'PLKJG51',
                        'incident_number': 4177,
                        'created_on': '2014-09-26T14:02:24Z',
                        'status': 'resolved',
                        'html_url': 'https://ambition.pagerduty.com/incidents/PLKJG51',
                        'incident_key': '44e5fad84a8b4effad1d940ca41efadd',
                        'service': {
                            'id': 'PPIYLHG',
                            'name': 'Ambition File Processor',
                            'html_url': 'https://ambition.pagerduty.com/services/PPIYLHG',
                            'deleted_at': None},
                        'escalation_policy': {
                            'id': 'PU2XJM5',
                            'name': 'Data Uploads',
                            'deleted_at': None},
                        'assigned_to_user': None,
                        'trigger_summary_data': {
                            'subject': 'False Alarm Description Field'},
                        'trigger_details_html_url':
                            'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R',
                        'trigger_type': 'web_trigger',
                        'last_status_change_on': '2014-09-26T14:03:50Z',
                        'last_status_change_by': {
                            'id': 'PC3L3KU',
                            'name': 'Wes Kendall',
                            'email': 'wes.kendall@ambition.com',
                            'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU'},
                        'number_of_escalations': 0,
                        'resolved_by_user': {
                            'id': 'PC3L3KU',
                            'name': 'Wes Kendall',
                            'email': 'wes.kendall@ambition.com',
                            'html_url': 'https://ambition.pagerduty.com/users/PC3L3KU'},
                        'assigned_to': []}},
                    'id': 'f13ab180-4585-11e4-a34d-22000ad9bf74',
                    'created_on': '2014-09-26T14:03:50Z'}]}

    def test_pagerduty_view(self):
        response = self.client.get('/pagerduty/')
        self.assertEqual(response.status_code, 200)

    def test_pagerdutyview_git(self):
        response = self.client.get('/pagerduty/')
        self.assertEqual(response.content, 'Pagerduty')

# ########### Test post ############

    @patch('ambition_slack.pagerduty.views.slack', spec_set=True)
    def test_multi_payload_triggered_resolved_closed(self, slack):
        inc_dtl_url = 'https://ambition.pagerduty.com/incidents/PLKJG51'
        trg_dtl_url = 'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R'
        inc_dtl_rs_url = 'https://ambition.pagerduty.com/incidents/PLKJG51'
        trg_dtl_rs_url = 'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R'

        # create a client & post the payload json to the client
        self.client.post(
            '/pagerduty/', json.dumps(self.example_multiple_payload),
            content_type='application/json')

        call_args_list = slack.chat.post_message.call_args_list
        # Verify that the post message was called twice
        self.assertEquals(len(call_args_list), 2)
        # Verify that the first call was for a triggered incident
        self.assertEquals(
            call_args_list[0],
            call(
                '#support',
                'New Pagerduty Ticket assigned to {}. Incident details - {}. Trigger details - {}'.format(
                    'Wes Kendall, Josh Marlow, Wayne Fullam', inc_dtl_url, trg_dtl_url),
                username='pagerduty')
        )
        self.assertEquals(
            call_args_list[1],
            call(
                '#support',
                'Pagerduty Ticket is now Resolved. Thank you. Incident details - {}. Trigger details - {}'.format(
                    inc_dtl_rs_url, trg_dtl_rs_url),
                username='pagerduty'
            )
        )

    @patch('ambition_slack.pagerduty.views.slack', spec_set=True)
    def test_single_payload_triggered(self, slack):
        inc_dtl_url = 'https://ambition.pagerduty.com/incidents/PLKJG51'
        trg_dtl_url = 'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R'
        # create a client & post the payload json to the client
        self.client.post(
            '/pagerduty/', json.dumps(self.example_single_trigger_payload),
            content_type='application/json')
        slack.chat.post_message.assert_called_with(
            '#support',
            'New Pagerduty Ticket assigned to {}. Incident details - {}. Trigger details - {}'.format(
                'Wes Kendall, Josh Marlow, Wayne Fullam', inc_dtl_url, trg_dtl_url),
            username='pagerduty')

    @patch('ambition_slack.pagerduty.views.slack', spec_set=True)
    def test_single_payload_resolved(self, slack):
        inc_dtl_rs_url = 'https://ambition.pagerduty.com/incidents/PLKJG51'
        trg_dtl_rs_url = 'https://ambition.pagerduty.com/incidents/PLKJG51/log_entries/P2S2I8R'
        # create a client & post the payload json to the client
        self.client.post(
            '/pagerduty/', json.dumps(self.example_single_resolve_payload),
            content_type='application/json')
        # Verify that slack posts a message
        slack.chat.post_message.assert_called_with(
            '#support',
            'Pagerduty Ticket is now Resolved. Thank you. Incident details - {}. Trigger details - {}'.format(
                inc_dtl_rs_url, trg_dtl_rs_url),
            username='pagerduty')
