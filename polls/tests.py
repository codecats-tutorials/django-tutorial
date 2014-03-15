from django.test import TestCase
import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse

from polls.models import Poll

def create_poll(question, days):
    return Poll.objects.create(question = question, pub_date = timezone.now() + datetime.timedelta(days = days))

class PullViewTests(TestCase):
    def test_index_view_with_no_pulls(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls')
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])
    def test_index_view_with_a_past_pool(self):
        create_poll('Past poll', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll>'])
    def test_index_view_with_a_future_poll(self):
        create_poll('Future poll', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls', status_code = 200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])
    def test_index_view_with_future_poll_and_past_poll(self):
        create_poll('Future poll', 30)
        create_poll('Past poll', -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll>'])
    def test_index_view_with_two_past_polls(self):
        create_poll('Past poll 1', -30)
        create_poll('Past poll 2', -5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_poll_list'], ['<Poll: Past poll 2>', '<Poll: Past poll 1>'])
        

class pullMethodTests(TestCase):
    def test_was_published_recently_with_future_poll(self):
        future_poll = Poll(pub_date = timezone.now() + datetime.timedelta(days = 30))
        self.assertEqual(future_poll.was_published_recently(), False)
        
    def test_was_published_recently_with_old_poll(self):
        old_poll = Poll(pub_date = timezone.now() - datetime.timedelta(days = 30))
        self.assertEqual(old_poll.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_poll(self):
        recently_poll = Poll(pub_date = timezone.now() - datetime.timedelta(hours = 2))
        self.assertEqual(recently_poll.was_published_recently(), True)