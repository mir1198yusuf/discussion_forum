from django.test import TestCase
from django.urls import reverse, resolve
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
import boards.views
from forms_dir.topicreply_form import TopicReply_Form

class TopicReplyPage_Test(TestCase):

	"""
	1. url status code, url name , func resolving for correct board id and topic id
	2. url for incorrect topic id but correct board id
	3. url for incorrect board id
	4. link to home page, board topicpage, topic page and reply page
	5. form csrf check
	6. form instance check
	7. form fields type and number check
	8. form fields sequence check
	9. correct data - post created - redirection 
	10. incorrect data - same page - post not created
	11. empty data - same page - post not created
	"""

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.user = User.objects.create_user(username='Test', email='test@test.com', password='test123')
		cls.topic = Topic.objects.create(subject='Test', board=cls.board, created_by=cls.user)
		cls.replytopicurl_correct = reverse('topic_reply_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.replytopicpath_correct = '/board/{}/topic/{}/reply/'.format(cls.board.id, cls.topic.id)
		cls.resolveresult = resolve(cls.replytopicpath_correct)
		cls.replytopicurl_wrongboard = reverse('topic_reply_url', kwargs={'board_id':99, 'topic_id':cls.topic.id})
		cls.replytopicurl_wrongtopic = reverse('topic_reply_url', kwargs={'board_id':cls.board.id, 'topic_id':99})
		cls.homeurl = reverse('home_url')
		cls.boardtopicsurl = reverse('board_topics_url', kwargs={'board_id':cls.board.id})
		cls.topicurl = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.formfields_seq = ['message']
		cls.replytopicdata_correct = {'message': 'Test message'}

	#login needed
	def setUp(self):
		self.client.login(username='Test', password='test123')

	def test_1(self):
		response = self.client.get(self.replytopicurl_correct)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'topic_reply_url')
		self.assertEqual(self.resolveresult.func, boards.views.topic_reply_page)

	def test_2(self):
		response = self.client.get(self.replytopicurl_wrongtopic)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		response = self.client.get(self.replytopicurl_wrongboard)
		self.assertEqual(response.status_code, 404)

	def test_4(self):
		response = self.client.get(self.replytopicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.boardtopicsurl))
		self.assertContains(response, 'href="{}"'.format(self.topicurl))
		self.assertContains(response, 'href="{}"'.format(self.replytopicurl_correct))

	def test_5(self):
		response = self.client.get(self.replytopicurl_correct)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_6(self):
		response = self.client.get(self.replytopicurl_correct)
		self.assertIsInstance(response.context.get('form'), TopicReply_Form)

	def test_7(self):
		response = self.client.get(self.replytopicurl_correct)
		self.assertContains(response, '<input type=', 1)	#csrf
		self.assertContains(response, '<textarea', 1)	#message

	def test_8(self):
		response = self.client.get(self.replytopicurl_correct)
		response_formfields_seq = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_formfields_seq, self.formfields_seq)

	def test_9(self):
		response = self.client.post(self.replytopicurl_correct, data=self.replytopicdata_correct, follow=True)
		self.assertTrue(Post.objects.exists())	#post created
		post = Post.objects.first()
		self.topicurl_with_page_id = '{url}?page={pageno}#{postid}'.format(url=self.topicurl, pageno=self.topic.get_last_posts_pageno(), postid=post.id)
		self.assertRedirects(response=response, expected_url=self.topicurl_with_page_id, status_code=302, target_status_code=200)	#redirected to topic page

	def test_10(self):
		response = self.client.post(self.replytopicurl_correct, data={})	#no follow
		self.assertFalse(Post.objects.exists())	#post not created
		self.assertEqual(response.status_code, 200)	#not 302 redirection

	def test_11(self):
		response = self.client.post(self.replytopicurl_correct, data={'message': ''})	#no follow
		self.assertFalse(Post.objects.exists())	#post not created
		self.assertEqual(response.status_code, 200)	#not 302 redirection





