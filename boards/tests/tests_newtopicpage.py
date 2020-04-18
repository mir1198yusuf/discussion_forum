from django.test import TestCase
from django.urls import reverse,resolve
from boards.models import Board, Topic, Post
from boards.views import new_topic
from django.contrib.auth.models import User
from forms_dir.newtopic_form import NewTopic_Form

class NewTopicPage_Test(TestCase):

	"""
	1. check if new_topic_url is giving correct status code 200 (correct board id)
	2. check if new_topic_url is giving correct status code 404 (incorrect board id)
	3. check if new topic url path is resolving to correct url name
	4. check if new topic url path is resolving to correct function name
	5. check if new topic page contains link to home page at breadcrumb navigation 
	6. check if new topic page contains link to topic page at breadcrumb navigation
	7. check if new topic page contains link to new topic page itself at breadcrumb navigation 
	8. check if csrf_token present in new topic page
	9. check if new topic/post created for valid data, logged in user is creater of topic/post, topic of post is currently created topic and redirects successful
	10. check if new topic/post not created for invalid data and no redirects
	11. check if new topic/post not created for empty  data and no redirects
	12. check if form class NewTopic_Form is used
	13. check on sequence of form fields
	14. check on number of form fields type
	15. check on login required to access this page
	"""

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.user = User.objects.create_user(username='Test', email='test@test.com', password='test123')
		cls.newtopicurl_correct = reverse('new_topic_url', kwargs={'board_id':cls.board.id})
		cls.newtopicurl_incorrect = reverse('new_topic_url', kwargs={'board_id': 99})
		cls.pathcorrect = '/board/' + str(cls.board.id) + '/newtopic/'
		cls.resolveresult = resolve(cls.pathcorrect)
		cls.homeurl = reverse('home_url')
		cls.boardtopicpageurl = reverse('board_topics_url', kwargs={'board_id': cls.board.id})
		cls.formfieldseq = ['subject','message']

	def setUp(self):
		#login user 
		self.client.login(username='Test', password='test123')

	def test_1(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		response = self.client.get(self.newtopicurl_incorrect)
		self.assertEqual(response.status_code, 404)

	def test_3(self):
		self.assertEqual(self.resolveresult.url_name, 'new_topic_url')

	def test_4(self):
		self.assertEqual(self.resolveresult.func, new_topic)

	def test_5(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))

	def test_6(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.boardtopicpageurl))

	def test_7(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertContains(response, 'href="{}"'.format(self.newtopicurl_correct))

	def test_8(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_9(self):
		response = self.client.post(self.newtopicurl_correct,follow=True, data={'subject':'Test', 'message':'Test'})
		self.assertTrue(Topic.objects.exists())	#has topic object created
		self.assertTrue(Post.objects.exists())	#has post object created
		#created_by of topic is logged in user 
		self.assertEqual(Topic.objects.get(subject='Test').created_by, response.context.get('user'))	#since this url is accessible only for logged in users, so context user is logged in user
		#created_by of post is logged in user 
		self.assertEqual(Post.objects.get(message='Test').created_by, response.context.get('user'))
		#verify topic of post
		self.assertEqual(Topic.objects.get(subject='Test'), Post.objects.get(message='Test').topic)
		topic = Topic.objects.first()
		topicpageurl = reverse('topic_page_url', kwargs={'board_id':self.board.id, 'topic_id':topic.id})
		self.assertRedirects(response=response, expected_url=topicpageurl, status_code=302, target_status_code=200)

	def test_10(self):
		response = self.client.post(self.newtopicurl_correct, data={})
		#here we passed invalid data , so it should not redirect and stay on same page
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())	
		#check not redirected because we use render() to display same page
		self.assertEqual(response.status_code, 200)
		#if there is redirect there will status code 30*...HttpResponse does not have url parameter
		#if status code is 200 , it means whatever render() is sending that is successful...see test_1

	def test_11(self):
		#here we pass empty fields 
		response = self.client.post(self.newtopicurl_correct, data={'subject': '', 'message':''})
		self.assertFalse(Topic.objects.exists())
		self.assertFalse(Post.objects.exists())
		self.assertEqual(response.status_code, 200)
		#for explanation see test_10

	def test_12(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertIsInstance(response.context.get('form'),NewTopic_Form)

	def test_13(self):
		response = self.client.get(self.newtopicurl_correct)	
		response_form_fields = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_form_fields, self.formfieldseq)

	def test_14(self):
		response = self.client.get(self.newtopicurl_correct)
		self.assertContains(response, '<input type=', 2)	#csrf and subject
		self.assertContains(response, 'type="text"', 1)	#subject
		self.assertContains(response, '<textarea', 1)	#message


