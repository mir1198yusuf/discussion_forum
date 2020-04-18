from django.test import TestCase
from django.urls import reverse, resolve
from boards.models import Board,Topic
from boards.views import board_topics

class BoardTopicPage_Test(TestCase):

	#1. check if board_topics_url is giving correct status code 200 (correct board id)
	#2. check if board_topics_url is giving correct status code 404 (incorrect board id)
	#3. check if board topic url path is resolving to correct url name
	#4. check if board topic url path is resolving to correct function name
	#5. check if board topic page contains link to home page at breadcrumb navigation 
	#6. check if board topic page contains link to topic page at breadcrumb navigation 
	#7. check if new topic url link present
	#8. check if topic url present in table

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.homeurl = reverse('home_url')
		cls.topicurl_correct = reverse('board_topics_url', kwargs={'board_id': cls.board.id})
		cls.topicurl_incorrect = reverse('board_topics_url', kwargs={'board_id':99})
		cls.newtopicurl_correct = reverse('new_topic_url', kwargs={'board_id': cls.board.id})
		cls.path_correct = '/board/' + str(cls.board.id) + '/'
		cls.resolveresult = resolve(cls.path_correct)
		cls.topic = Topic.objects.create(subject='Test',board=cls.board)
		cls.topicpageurl = reverse('topic_page_url', kwargs={'board_id':cls.board.id, 'topic_id':cls.topic.id})
		
	def test_1(self):
		response = self.client.get(self.topicurl_correct)
		self.assertEqual(response.status_code, 200)

	def test2(self):
		response = self.client.get(self.topicurl_incorrect)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		self.assertEqual(self.resolveresult.url_name, 'board_topics_url')

	def test_4(self):
		self.assertEqual(self.resolveresult.func, board_topics)

	def test_5(self):
		response = self.client.get(self.topicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))

	def test_6(self):
		response = self.client.get(self.topicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.topicurl_correct))

	def test_7(self):
		response = self.client.get(self.topicurl_correct)
		self.assertContains(response, self.newtopicurl_correct)

	def test_8(self):
		response = self.client.get(self.topicurl_correct)
		self.assertContains(response, self.topicpageurl)

