from django.test import TestCase
from django.urls import reverse,resolve
import user_account.views 
from django.contrib.auth.models import User
from forms_dir.signup_form import SignUp_Form

class SignUpPage_Test(TestCase):

	"""
	1. check if getting status code 200 for signup url
	2. check if getting correct url name for sign up url path
	3. check if getting correct function name for sign up path
	4. check for csrf token
	5. check for form SignUp_Form instance
	6. check if user created, has user logged in and redirects for correct data, since user is now logged in he should not be able to access signup page
		instead should get redirected to home page 
	7. check if user not created and no redirect for invalid data
	8. check if user not created and no redirect for empty data in field
	9. check number of fields and their types in form
	10. check sequence of fields in form
	11. check if there is link to home page, signup in navigation bar
	12. check if there is link to login page in top bar
	"""
	
	@classmethod
	def setUpTestData(cls):
		cls.signupurl = reverse('signup_url')
		cls.loginurl = reverse('login_url')
		cls.signup_path = '/user/signup/'
		cls.resolveresult = resolve(cls.signup_path)
		cls.signupdata = {'username':'Test','email':'test@test.com' ,'password1':'mynameisTest123', 'password2':'mynameisTest123'}
		cls.homeurl = reverse('home_url')
		cls.formfield_seq = ['username','email', 'password1', 'password2']

	def test_1(self):
		response = self.client.get(self.signupurl)
		self.assertEqual(response.status_code, 200)

	def test_2(self):
		self.assertEqual(self.resolveresult.url_name, 'signup_url')

	def test_3(self):
		self.assertEqual(self.resolveresult.func, user_account.views.signupuser)

	def test_4(self):
		response = self.client.get(self.signupurl)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_5(self):
		response = self.client.get(self.signupurl)
		self.assertIsInstance(response.context.get('form'), SignUp_Form)

	def test_6(self):
		response = self.client.post(self.signupurl, data=self.signupdata, follow=True)
		self.assertTrue(User.objects.exists())	#user created`=>>> if this fails print errors
		self.assertTrue(response.context.get('user').is_authenticated)  #user logged in
		#user redirected to home page
		self.assertRedirects(response=response, expected_url=self.homeurl, status_code=302, target_status_code=200)
		#now if user tries to access sign up page , he should get redirected to home page since he is already logged in
		response = self.client.get(self.signupurl)
		self.assertRedirects(response=response, expected_url=self.homeurl, status_code=302, target_status_code=200)

	def test_7(self):
		response = self.client.post(self.signupurl, data={})
		self.assertFalse(User.objects.exists())	#user not created
		self.assertEqual(response.status_code, 200)	#not 302 means not redirected

	def test_8(self):
		response = self.client.post(self.signupurl, data={'username':'','email':'', 'password1':'', 'password2':''})
		self.assertFalse(User.objects.exists())	#user not created
		self.assertEqual(response.status_code, 200)		#not 302 means not redirected

	def test_9(self):
		response = self.client.get(self.signupurl)
		self.assertContains(response, '<input type', 5)	#csrf,username,email,password,confirm_password
		self.assertContains(response, 'type="text"', 1)	#username
		self.assertContains(response, 'type="email"', 1)	#email	
		self.assertContains(response, 'type="password', 2)	#password, confirm_password

	def test_10(self):
		response = self.client.get(self.signupurl)	
		response_form_fields = list(response.context.get('form').fields.keys())	#expr. obtained by dir and type
		self.assertSequenceEqual(response_form_fields,self.formfield_seq)

	def test_11(self):
		response = self.client.get(self.signupurl)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.signupurl))

	def test_12(self):
		response = self.client.get(self.signupurl)
		self.assertContains(response, 'href="{}"'.format(self.loginurl))
