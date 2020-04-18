from django.test import TestCase
from django.urls import reverse,resolve
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
from boards.views import PostEdit_View
from forms_dir.postedit_form import PostEdit_Form

class EditPostPage_Test(TestCase):

	"""
	1. url accessible, status code, url_name and function resolving - all correct args
	2. url accessible - correct board and topic but incorrect post id
	3. url accessible for incorrect topic but correct board
	4. url accessible for incorrect board
	5. home link, board topics list, topic page and edit link in navigation bar
	6. form csrf check
	7. form instance check
	8. form fields number and type check
	9. form fields sequence check
	10. cancel link present
	11. empty data - same page rendering
	12. incorrect data - same page rendering
	13. correct data - post edited and redirection
	14. check if any other user can edit someone else's post
	"""

	@classmethod
	def setUpTestData(cls):
		cls.user1 = User.objects.create_user(username='test1', email='test1@test.com', password='test123')
		cls.user2 = User.objects.create_user(username='test2', email='test2@test.com', password='test456')
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.topic = Topic.objects.create(subject='Test', board=cls.board, created_by=cls.user1)
		cls.post1 = Post.objects.create(message='Test1', topic=cls.topic, created_by=cls.user1)
		cls.post2 = Post.objects.create(message='Test2', topic=cls.topic, created_by=cls.user2)
		cls.homeurl = reverse('home_url')
		cls.boardtopics_url = reverse('board_topics_url', kwargs={'board_id':cls.board.id})
		cls.topicpageurl = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.editposturl_correct = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id, 'post_id':cls.post1.id})
		cls.editposturl_wrongboard = reverse('post_edit_url', kwargs={'board_id':99, 'topic_id':cls.topic.id, 'post_id':cls.post1.id})
		cls.editposturl_wrongtopic = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':99, 'post_id':cls.post1.id})
		cls.editposturl_wrongpost = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id, 'post_id':99})
		cls.editpostpath_correct = '/board/{}/topic/{}/post/{}/edit/'.format(cls.board.id, cls.topic.id, cls.post1.id)
		cls.resolveresult = resolve(cls.editpostpath_correct)
		cls.formfields_seq = ['message']
		cls.cancelediturl = '{url}?page={pageno}#{postid}'.format(url=cls.topicpageurl, pageno=cls.topic.get_pageno_of_post(cls.post1), postid=cls.post1.id)

	def setUp(self):
		self.client.login(username='test1', password='test123')

	def test_1(self):
		response = self.client.get(self.editposturl_correct)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'post_edit_url')
		self.assertEqual(self.resolveresult.func.__name__, PostEdit_View.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.editposturl_wrongpost)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		response = self.client.get(self.editposturl_wrongtopic)
		self.assertEqual(response.status_code, 404)

	def test_4(self):
		response = self.client.get(self.editposturl_wrongboard)
		self.assertEqual(response.status_code, 404)

	def test_5(self):
		response = self.client.get(self.editposturl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.boardtopics_url))
		self.assertContains(response, 'href="{}"'.format(self.topicpageurl))
		self.assertContains(response, 'href="{}"'.format(self.editposturl_correct))

	def test_6(self):
		response = self.client.get(self.editposturl_correct)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_7(self):
		response = self.client.get(self.editposturl_correct)
		self.assertIsInstance(response.context.get('form'), PostEdit_Form)

	def test_8(self):
		response = self.client.get(self.editposturl_correct)
		self.assertContains(response, '<input type=',1)	#csrf
		self.assertContains(response, '<textarea', 1)	#message

	def test_9(self):
		response = self.client.get(self.editposturl_correct)
		response_formfields_seq = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_formfields_seq, self.formfields_seq)

	def test_10(self):
		response = self.client.get(self.editposturl_correct)
		self.assertContains(response, 'href="{}"'.format(self.cancelediturl), 1)	

	def test_11(self):
		response = self.client.post(self.editposturl_correct, data={'message':''})	#no follow
		self.assertEqual(response.status_code, 200)	#not 302 redirection

	def test_12(self):
		response = self.client.post(self.editposturl_correct, data={})	#no follow
		self.assertEqual(response.status_code, 200)	#not 302 redirection		

	def test_13(self):
		response = self.client.post(self.editposturl_correct, data={'message':'Edit message'}, follow=True)
		self.assertTrue(Post.objects.filter(message='Edit message').exists())	#new message is updated
		self.assertFalse(Post.objects.filter(message='Test1').exists())	#old message object does not exist
		#the above two checks are to see if object is updated and not a new one created
		topicurl_pageid = '{url}?page={pageno}#{postid}'.format(url=self.topicpageurl, pageno=self.topic.get_pageno_of_post(self.post1), postid=self.post1.id)
		self.assertRedirects(response=response, expected_url=topicurl_pageid, status_code=302, target_status_code=200)

	def test_14(self):
		#since post1 created by user 1 , he can edit it 
		#but using correct url, user2 should not be able to edit it
		#first we login with user 2
		self.client.login(username='test2', password='test456')
		response = self.client.get(self.editposturl_correct)
		self.assertEqual(response.status_code, 404)	#page not found
