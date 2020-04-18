from django.test import TestCase
from django.urls import reverse, resolve
from boards.views import Home_View
from boards.models import Board

# Create your tests here.

class HomePage_Test(TestCase):
	
	#1. check if home_url is giving correct status code 200
	#2. check if home url path is resolving to correct url name
	#3. check if home url path is resolving to correct function name
	#4. check if home page contains link to home page at breadcrumb navigation 
	#5. check if home page contains link to topic in table

	@classmethod
	def setUpTestData(cls):
		cls.board = Board.objects.create(name='Test', description='Test')
		cls.home_url = reverse('home_url')
		cls.boardtopics_url = reverse('board_topics_url', kwargs={'board_id':cls.board.id})
		cls.path = '/'
		cls.resolveresult = resolve(cls.path)

	def test_1(self):
		response = self.client.get(self.home_url)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		self.assertEqual(self.resolveresult.url_name, 'home_url')
		#since here it returns url name as string so we directly compare w/o importing

	def test_3(self):
		self.assertEqual(self.resolveresult.func.__name__, Home_View.as_view().__name__)
		#here it returns function not as string...so we have to import function to match

	def test_4(self):
		response = self.client.get(self.home_url)
		self.assertContains(response, 'href="{}"'.format(self.home_url))

	def test_5(self):
		response = self.client.get(self.home_url)
		self.assertContains(response, 'href="{}"'.format(self.boardtopics_url))
