from django.test import TestCase
from boards.models import Board,Topic,Post
from django.urls import reverse
from django.contrib.auth.models import User

class BoardsLoginRequired_Test(TestCase):

	"""
	1. is new topic page cannot accessible w/o login
	2. is topic reply page accessible w/o login
	3. is post edit page accessible w/o login -
 	"""

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='Test', email='test@test.com', password='test123')
		cls.board = Board.objects.create(name='TestBoard',description='TestBoardDescription')
		cls.topic = Topic.objects.create(subject='Test', board=cls.board, created_by=cls.user)
		cls.post = Post.objects.create(message='Test', topic=cls.topic, created_by=cls.user)
		cls.newtopicurl = reverse('new_topic_url', kwargs={'board_id':cls.board.id})
		cls.loginurl = reverse('login_url')
		cls.replytopicurl = reverse('topic_reply_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		cls.editposturl = reverse('post_edit_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id, 'post_id':cls.post.id})

	def test_1(self):
		response = self.client.get(self.newtopicurl, follow=True)
		redirected_url = self.loginurl + '?next=' + self.newtopicurl
		self.assertRedirects(response=response,expected_url=redirected_url, status_code=302, target_status_code=200)

	def test_2(self):
		response = self.client.get(self.replytopicurl, follow=True)
		redirected_url = self.loginurl + '?next=' + self.replytopicurl
		self.assertRedirects(response=response, expected_url=redirected_url, status_code=302, target_status_code=200)
		
	def test_3(self):
		response = self.client.get(self.editposturl, follow=True)
		redirected_url = self.loginurl + '?next=' + self.editposturl
		self.assertRedirects(response=response, expected_url=redirected_url, status_code=302, target_status_code=200)
