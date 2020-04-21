from django.test import TestCase
from django.urls import reverse,resolve
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from discussion_forum.settings import DEFAULT_FROM_EMAIL
from user_account.views import NewPasswordReset_View

class PasswordReset_Test(TestCase):

	"""
	1. check url status code, url_name, fucntion resolving 
	2. check link to login on to bar
	3. check link to home and password reset on navigation bar
	4. form instance check
	5. csrf  check
	6. form field type and number check
	7. form field sequence check
	8. posting of invalid data check - email not present in User model, check email not delivered but redirection happens
	9. posting of valid email data - email present in User model, check email delivered or not,
		redirected to link sent page
		also email subject verify, email sender verify, email recipient verify, email following content verify :
		username, email, link  
	10. posting of invalid data - empty fields
	"""
	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='test',email='test@test.com',password='test123')
		cls.passwordreseturl = reverse('password_reset_url')
		cls.passwordresetsenturl = reverse('password_reset_sent_url')
		cls.passwordresetpath = '/user/passwordreset/'
		cls.resolveresult = resolve(cls.passwordresetpath)
		cls.loginurl = reverse('login_url')
		cls.homeurl = reverse('home_url')
		cls.resetdata_correct = {'email':'test@test.com'}	
		cls.resetdata_incorrect = {'email':'test1@test.com'}
		cls.formfields_seq = ['email']

	def test_1(self):
		response = self.client.get(self.passwordreseturl)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'password_reset_url')
		self.assertEqual(self.resolveresult.func.__name__, NewPasswordReset_View.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.passwordreseturl)
		self.assertContains(response, 'href="{}"'.format(self.loginurl))

	def test_3(self):
		response = self.client.get(self.passwordreseturl)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.passwordreseturl))

	def test_4(self):
		response = self.client.get(self.passwordreseturl)
		self.assertIsInstance(response.context.get('form'),PasswordResetForm)

	def test_5(self):
		response = self.client.get(self.passwordreseturl)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_6(self):
		response = self.client.get(self.passwordreseturl)
		self.assertContains(response, '<input type=', 2)	#csrf email
		self.assertContains(response, 'type="email"', 1)	#email

	def test_7(self):
		response = self.client.get(self.passwordreseturl)
		response_formfield_seq = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_formfield_seq, self.formfields_seq)

	def test_8(self):
		response = self.client.post(self.passwordreseturl, data=self.resetdata_incorrect, follow=True)
		#since no user with this email, email not delivered
		self.assertEqual(len(mail.outbox),0)	#no email in outbox
		#check redirection happens
		self.assertRedirects(response=response,expected_url=self.passwordresetsenturl, status_code=302,target_status_code=200)

	def test_9(self):
		response = self.client.post(self.passwordreseturl,data=self.resetdata_correct)
		self.assertEqual(len(mail.outbox),1)	#email should be sent as email is valid
		#check redirection happens
		self.assertRedirects(response=response,expected_url=self.passwordresetsenturl, status_code=302,target_status_code=200)
		#get first instance from outbox
		reset_email = mail.outbox[0]
		#check subject of reset_email
		#THIS BELOW IS FOR CONSOLE EMAIL BACKEND
		self.assertEqual('[Discussion Forum] Please reset your password', reset_email.subject)
		#check reset_email sender
		self.assertEqual(DEFAULT_FROM_EMAIL,reset_email.from_email)
		#check reset email recipient 
		self.assertEqual(self.resetdata_correct.get('email'),reset_email.to[0])
		#check if username in reset email body
		self.assertIn(self.user.username,reset_email.body)
		#check if email in reset email body
		self.assertIn(self.user.email,reset_email.body)
		#check if reset link present in reset email body
		##if follow=False in response we can get token/uid which was passed from resetpassword to resetpasswordsent page
		uidb64 = response.context.get('uid')
		token = response.context.get('token')
		reset_link = reverse('password_reset_update_url',kwargs={'uidb64':uidb64, 'token':token})
		self.assertIn(reset_link,reset_email.body)

	def test_10(self):
		response = self.client.post(self.passwordreseturl, data={})	#no follow here
		self.assertEqual(response.status_code, 200)	#no 302 redirection

