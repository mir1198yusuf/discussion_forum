from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.views import PasswordResetCompleteView

class ResetPasswordDone_Test(TestCase):

	"""
	1. url status code, url_name and function resolving
	2. link to home page, reset done page in navigation bar
	3. link to login in top bar
	4. reset success msg
	"""

	@classmethod
	def setUpTestData(cls):
		cls.resetpassworddoneurl = reverse('password_reset_done_url')
		cls.resetpassworddonepath = '/user/passwordreset/done/'
		cls.resolveresult = resolve(cls.resetpassworddonepath)
		cls.homeurl = reverse('home_url')
		cls.loginurl = reverse('login_url')

	def test_1(self):
		response = self.client.get(self.resetpassworddoneurl)
		self.assertEqual(response.status_code,200)
		self.assertEqual(self.resolveresult.func.__name__, PasswordResetCompleteView.as_view().__name__)
		self.assertEqual(self.resolveresult.url_name, 'password_reset_done_url')

	def test_2(self):
		response = self.client.get(self.resetpassworddoneurl)
		self.assertContains(response, self.homeurl)
		self.assertContains(response, self.resetpassworddoneurl)

	def test_3(self):
		response = self.client.get(self.resetpassworddoneurl)
		self.assertContains(response, self.loginurl)

	def test_4(self):
		response = self.client.get(self.resetpassworddoneurl)
		self.assertContains(response, 'Your password has been successfully resetted')
