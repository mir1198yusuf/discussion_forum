from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class HomePage_Test(TestCase):

	"""
	1. home page has urls to sign up and login page 
	2. home page has dropdown-username if user is logged in and also links to myaccount, changepassword and logout
	"""

	@classmethod
	def setUpTestData(cls):
		cls.signupurl = reverse('signup_url')
		cls.loginurl = reverse('login_url')
		cls.homeurl = reverse('home_url')
		cls.changepasswordurl = reverse('password_change_url')
		cls.logouturl = reverse('logout_url')
		cls.profileurl = reverse('myprofile_update_url')
		cls.user = User.objects.create_user(username='Test', email='test@test.com', password='test123')

	def test_1(self):
		#user not logged in
		response = self.client.get(self.homeurl)
		self.assertContains(response, 'href="{}"'.format(self.signupurl))
		self.assertContains(response, 'href="{}"'.format(self.loginurl))

	def test_2(self):
		#user is logged in 
		self.client.login(username='Test', password='test123')
		response = self.client.get(self.homeurl)
		#search for user name of currently logged in user
		self.assertContains(response, response.context.get('user').username)
		self.assertContains(response, 'href="{}"'.format(self.changepasswordurl))	#change password link
		self.assertContains(response, 'href="{}"'.format(self.logouturl)) #logout link
		self.assertContains(response, 'href="{}"'.format(self.profileurl)) #my account link

	