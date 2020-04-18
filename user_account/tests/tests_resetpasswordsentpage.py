from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.views import PasswordResetDoneView

class ResetPasswordSent_Test(TestCase):

	"""
	1. url status code, resolve urlname and function
	2. links to home, reset password, 'reset link sent' link in navigation bar
	3. link to login page in top bar
	"""

	@classmethod
	def setUpTestData(cls):
		cls.homeurl = reverse('home_url')
		cls.resetpasswordurl = reverse('password_reset_url')
		cls.resetpasswordsenturl = reverse('password_reset_sent_url')
		cls.resetpasswordsentpath = '/user/passwordreset/sent/'
		cls.resolveresult = resolve(cls.resetpasswordsentpath)
		cls.loginurl = reverse('login_url')

	def test_1(self):
		response = self.client.get(self.resetpasswordsenturl)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'password_reset_sent_url')
		self.assertEqual(self.resolveresult.func.__name__, PasswordResetDoneView.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.resetpasswordsenturl)
		self.assertContains(response,self.homeurl)
		self.assertContains(response,self.resetpasswordurl)
		self.assertContains(response,self.resetpasswordsenturl)

	def test_3(self):
		response = self.client.get(self.resetpasswordsenturl)
		self.assertContains(response,self.loginurl)

