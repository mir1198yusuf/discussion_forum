from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User

class Logout_Test(TestCase):

	"""
	1. logout url resolving to correct urlname and function
	2. if user logged in, logout url will logged out him and redirect to home page
	"""

	@classmethod
	def setUpTestData(cls):
		cls.logouturl = reverse('logout_url')
		cls.logoutpath = '/user/logout/'
		cls.homeurl = reverse('home_url')
		cls.resolveresult = resolve(cls.logoutpath)
		cls.user = User.objects.create_user(username='test', email='test@test.com', password='test123')

	def test_1(self):
		self.assertEqual(self.resolveresult.url_name, 'logout_url')
		self.assertEqual(self.resolveresult.func.__name__, LogoutView.as_view().__name__)

	def test_2(self):
		#login() returns True if successful		
		loginresult = self.client.login(username='test', password='test123')
		self.assertTrue(loginresult)	# now we can assure that user is logged in 
		#but once we will logout the user context of response will have anonymous user assigned to it
		#so is_authenticated will always be false ..that correct but to check what is is_authenticated now after login , 
		#we call home url. remember there is no need for this as we can assure with login() result but to test more thoroughly
		response = self.client.get(self.homeurl)
		self.assertTrue(response.context.get('user').is_authenticated)
		response_logout = self.client.get(self.logouturl, follow=True)	#now we logout
		response = self.client.get(self.homeurl)
		self.assertFalse(response.context.get('user').is_authenticated) #this will now be false
		#redirection test - using 2nd response ie logout response 
		self.assertRedirects(response=response_logout, expected_url=self.homeurl, status_code=302, target_status_code=200)
