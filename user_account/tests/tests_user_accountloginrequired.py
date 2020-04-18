from django.test import TestCase
from django.urls import reverse

class User_AccountLoginRequired_Test(TestCase):

	"""
	1. change password url needs login
	2. change password done url needs login
	3. my account link url needs login
	"""

	@classmethod
	def setUpTestData(cls):
		cls.changepasswordurl = reverse('password_change_url')
		cls.changepassworddoneurl = reverse('password_change_done_url')
		cls.profilepageurl = reverse('myprofile_update_url')
		cls.loginurl = reverse('login_url')

	def test_1(self):
		response = self.client.get(self.changepasswordurl, follow=True)
		redirected_url = self.loginurl + '?next=' + self.changepasswordurl
		self.assertRedirects(response=response, expected_url=redirected_url, status_code=302, target_status_code=200)

	def test_2(self):
		response = self.client.get(self.changepassworddoneurl, follow=True)
		redirected_url = self.loginurl + '?next=' + self.changepassworddoneurl
		self.assertRedirects(response=response, expected_url=redirected_url, status_code=302, target_status_code=200)

	def test_3(self):
		response = self.client.get(self.profilepageurl, follow=True)
		redirected_url = self.loginurl + '?next=' + self.profilepageurl	
		self.assertRedirects(response=response, expected_url=redirected_url, status_code=302, target_status_code=200)
