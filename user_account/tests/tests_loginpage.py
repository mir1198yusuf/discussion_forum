from django.test import TestCase
from django.urls import reverse, resolve 
import django.contrib.auth.views as django_auth_views
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class LoginPage_Test(TestCase):

	"""
	1. is login url status code 200
	2. is login url's url name resolving correct
	3. is login url function name resolving correct
	4. is login failed for invalid data and same page displayed
	5. is login correct for valid data, has user logged in and redirected to home_page
	6. form instance is correct
	7. csrf token check
	8. form fields sequence check
	9. form fields number and type check
	10. link to home page in navigation bar
	11. link to login page in navigation bar
	12. link to signup page in top bar
	13. forget password link present
	"""

	@classmethod
	def setUpTestData(cls):
		cls.loginurl = reverse('login_url')
		cls.homeurl = reverse('home_url')
		cls.signupurl = reverse('signup_url')
		cls.passwordreseturl = reverse('password_reset_url')
		cls.loginpath = '/user/login/'
		cls.resolveresult = resolve(cls.loginpath)
		cls.user = User.objects.create_user(username='Test', email='test@test.com', password='test123')
		cls.logindata_correct = {'username':'Test', 'password':'test123'}
		cls.formfields_seq = ['username', 'password']

	def test_1(self):
		response = self.client.get(self.loginurl)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		self.assertEqual(self.resolveresult.url_name, 'login_url')

	def test_3(self):
		#below will always be false because as_views() returns a new fucntion each time at different memory address..so name will be same but not id
		#self.assertEqual(self.resolveresult.func, django_auth_views.LoginView.as_view())
		self.assertEqual(self.resolveresult.func.__name__, django_auth_views.LoginView.as_view().__name__)
		#so we compared names here

	def test_4(self):
		response = self.client.post(self.loginurl, data={})	#no follow here
		self.assertEqual(response.status_code, 200)	#not 302 redirection

	def test_5(self):
		response = self.client.post(self.loginurl, data=self.logindata_correct, follow=True)
		self.assertTrue(response.context.get('user').is_authenticated)	#user is logged in
		self.assertRedirects(response=response, expected_url=self.homeurl, status_code=302, target_status_code=200)

	def test_6(self):
		response = self.client.get(self.loginurl)
		self.assertIsInstance(response.context.get('form'), AuthenticationForm)

	def test_7(self):
		response = self.client.get(self.loginurl)
		self.assertContains(response, 'name="csrfmiddlewaretoken"')

	def test_8(self):
		response = self.client.get(self.loginurl)
		response_form_fields = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_form_fields, self.formfields_seq)

	def test_9(self):
		response = self.client.get(self.loginurl)
		self.assertContains(response, '<input type=', 3)	#csrf, username , password
		self.assertContains(response, 'type="text"', 1)	#username
		self.assertContains(response, 'type="password"', 1)	#password

	def test_10(self):
		response = self.client.get(self.loginurl)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))

	def test_11(self):
		response = self.client.get(self.loginurl)
		self.assertContains(response, 'href="{}"'.format(self.loginurl))

	def test_12(self):
		response = self.client.get(self.loginurl)
		self.assertContains(response, 'href="{}"'.format(self.signupurl))

	def test_13(self):
		response = self.client.get(self.loginurl)
		self.assertContains(response, 'href="{}"'.format(self.passwordreseturl))
