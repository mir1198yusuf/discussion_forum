from django.test import TestCase
from django.urls import reverse,resolve
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
import boards.views

class TopicPage_Test(TestCase):

	"""
	1. url status code, func , url_name resolving for correct board id and topic id
	2. url status code for correct board id and wrong topic id
	3. url status code for wrong board id
	4. home url, board topic url, topicpage url present in navigation bar
	5. reply link present
	6. check edit link present for creater user only 
	"""

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.user1 = User.objects.create_user(username='Test', email='test@test.com', password='test123')
		cls.topic = Topic.objects.create(subject='Test', board=cls.board, created_by=cls.user1)
		cls.post = Post.objects.create(message='Test', topic=cls.topic, created_by=cls.user1)
		cls.topicpageurl_correct = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.topicpagepath_correct = '/board/{board_id}/topic/{topic_id}/'.format(board_id=cls.board.id, topic_id=cls.topic.id)
		cls.resolveresult = resolve(cls.topicpagepath_correct)
		cls.topicpageurl_wrongboard = reverse('topic_page_url', kwargs={'board_id':99, 'topic_id':cls.topic.id})
		cls.topicpageurl_wrongtopic = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':99})
		cls.homeurl = reverse('home_url')
		cls.boardtopicurl = reverse('board_topics_url', kwargs={'board_id':cls.board.id})
		cls.replytopicurl = reverse('topic_reply_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.editposturl_correct = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id, 'post_id':cls.post.id})

	def test_1(self):
		response = self.client.get(self.topicpageurl_correct)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'topic_page_url')
		self.assertEqual(self.resolveresult.func.__name__, boards.views.TopicPage_View.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.topicpageurl_wrongtopic)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		response = self.client.get(self.topicpageurl_wrongboard)
		self.assertEqual(response.status_code, 404)

	def test_4(self):
		response = self.client.get(self.topicpageurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.boardtopicurl))
		self.assertContains(response, 'href="{}"'.format(self.topicpageurl_correct))

	def test_5(self):
		response = self.client.get(self.topicpageurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.replytopicurl))

	def test_6(self):
		#user1 is creator of post but he is not logged in
		#so he should not see the edit link now
		response = self.client.get(self.topicpageurl_correct)
		self.assertNotContains(response, 'href="{}"'.format(self.editposturl_correct))
		#now login and he should see it now
		self.client.login(username='Test', password='test123')
		response = self.client.get(self.topicpageurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.editposturl_correct))
