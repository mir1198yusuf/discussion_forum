from django.test import TestCase
from django.urls import reverse,resolve
#from django.contrib.auth import authenticate
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ChangePassword_Test(TestCase):

	"""
	1. change password link accessible status code 200, url name and fucntion resolving check
	2. link to home page in navigation bar
	3. link to change password in navigation bar
	4. logged in user name in top bar
	5. form fields sequence
	6. form fields type and number check
	7. csrf check
	8. posting with invalid data, same page rendered 
	9. posting with valid data, password changed and redirected to change password done page. user status logged in
	10. form instance check
	"""

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='test',email='test@test.com',password='test123')
		cls.homeurl = reverse('home_url')
		cls.changepasswordurl = reverse('password_change_url')
		cls.changepassworddoneurl = reverse('password_change_done_url')
		cls.changepasswordpath = '/user/changepassword/'
		cls.resolveresult = resolve(cls.changepasswordpath)
		cls.formfield_seq = ['old_password', 'new_password1','new_password2']
		cls.changepassworddata_correct = {'old_password':'test123', 'new_password1':'mynameisTest1', 'new_password2':'mynameisTest1'}

	def setUp(self):	#because login is required
		#change password possible only when user logged in
		self.client.login(username='test', password='test123')

	def test_1(self):
		response = self.client.get(self.changepasswordurl)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'password_change_url')
		self.assertEqual(self.resolveresult.func.__name__, PasswordChangeView.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.changepasswordurl)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))

	def test_3(self):
		response = self.client.get(self.changepasswordurl)
		self.assertContains(response, 'href="{}"'.format(self.changepasswordurl))

	def test_4(self):
		response = self.client.get(self.changepasswordurl)
		self.assertContains(response, response.context.get('user').username)

	def test_5(self):
		response = self.client.get(self.changepasswordurl)
		response_formfields = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_formfields, self.formfield_seq)

	def test_6(self):
		response = self.client.get(self.changepasswordurl)
		self.assertContains(response, '<input type', 4)	#csrf oldpassword newpassword1 newpassword2
		self.assertContains(response, 'type="password"', 3)	#oldpassword newpassword1 newpassword2

	def test_7(self):
		response = self.client.get(self.changepasswordurl)
		self.assertContains(response, 'name="csrfmiddlewaretoken"')

	def test_8(self):
		response = self.client.post(self.changepasswordurl, data={}, follow=True)
		self.assertEqual(response.status_code, 200)	#not 302 redirection

	def test_9(self):
		response = self.client.post(self.changepasswordurl, data=self.changepassworddata_correct, follow=True)
		##1st method - authenticate()
		#we cannot directly compare old and new password because old cannot be retrieved because of hash form
		#self.assertIsNotNone(authenticate(username='test',password='mynameisTest1'))	#new password object exists
		#self.assertIsNone(authenticate(username='test',password='test123'))	#old password object doesnot exist
		#BTW authenticate returns user object if user found
		##2nd method - refresh_from_db()
		#new password for this user in db
		#but old password in user object
		self.user.refresh_from_db()	
		self.assertTrue(self.user.check_password('mynameisTest1'))	#new password
		self.assertTrue(response.context.get('user').is_authenticated)	#user is logged in after change password
		self.assertRedirects(response=response, expected_url=self.changepassworddoneurl, status_code=302, target_status_code=200)	#check redirection

	def test_10(self):
		response = self.client.get(self.changepasswordurl)
		self.assertIsInstance(response.context.get('form'), PasswordChangeForm)

