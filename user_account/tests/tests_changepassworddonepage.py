from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.views import PasswordChangeDoneView
from django.contrib.auth.models import User

class ChangePasswordDone_Test(TestCase):

	"""
	1. check if changepassword done url is accessible, resolve url_name and function
	2. check if it has home link, change password link and change password done link in navigation bar
	3. check if username in top bar
	"""

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='test', email='test@test.com', password='test123')
		cls.homeurl = reverse('home_url')
		cls.changepasswordurl = reverse('password_change_url')
		cls.changepassworddoneurl = reverse('password_change_done_url')
		cls.changepassworddonepath = '/user/changepassword/done/'
		cls.resolveresult = resolve(cls.changepassworddonepath)

	def setUp(self):	#because login is required
		self.client.login(username='test',password='test123')

	def test_1(self):
		response = self.client.get(self.changepassworddoneurl)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'password_change_done_url')
		self.assertEqual(self.resolveresult.func.__name__, PasswordChangeDoneView.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.changepassworddoneurl)
		self.assertContains(response,'href="{}"'.format(self.homeurl))
		self.assertContains(response,'href="{}"'.format(self.changepasswordurl))
		self.assertContains(response,'href="{}"'.format(self.changepassworddoneurl))

	def  test_3(self):
		response = self.client.get(self.changepassworddoneurl)
		self.assertContains(response, response.context.get('user').username)

