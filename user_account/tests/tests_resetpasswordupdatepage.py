from django.test import TestCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from django.urls import reverse,resolve
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm

class ResetPasswordUpdate_Test(TestCase):

	"""
	1. url status code, resolve urlname and fucntion
	2. link to home, current page in navigation bar
	3. link to login at top bar
	4. invalid link - invalid message check
	5. invalid link - 'goto reset password' link
	6. valid link - form instance
	7. valid link - form field sequence
	8. valid link - form field type and number
	9. valid link -  csrf check
	10. valid link - valid data, check redirect, check password changed or not
	11. valid link - invalid data
	"""

	@classmethod
	def setUpTestData(cls):
		cls.homeurl = reverse('home_url')
		cls.loginurl = reverse('login_url')
		cls.resetpasswordurl = reverse('password_reset_url')
		cls.resetpassworddoneurl = reverse('password_reset_done_url')
		cls.resetpassworddata_correct = {'new_password1':'mynametestabc1', 'new_password2':'mynametestabc1'}	#new password for user1 not user 2
		#user to use for valid link
		cls.user1 = User.objects.create_user(username='test1',email='test1@test.com',password='test123')
		#user to use for invalid link
		cls.user2 = User.objects.create_user(username='test2',email='test2@test.com',password='test456')
		cls.valid_link, cls.valid_token, cls.valid_uid = ResetPasswordUpdate_Test.generate_valid_link_token_uid(cls.user1)
		cls.invalid_link,cls.invalid_token,cls.invalid_uid = ResetPasswordUpdate_Test.generate_invalid_link_token_uid(cls.user2)
		cls.valid_link_path = '/user/passwordreset/{uidb64}/{token}/'.format(uidb64=cls.valid_uid, token=cls.valid_token)
		cls.resolveresult = resolve(cls.valid_link_path)
		cls.formfields_seq = ['new_password1','new_password2']

	@staticmethod
	def generate_valid_link_token_uid(user):
		#generation of token and uidb64 based on below link : that is how django does that internally
		#https://github.com/django/django/blob/stable/2.2.x/django/contrib/auth/forms.py L299
		token = default_token_generator.make_token(user)
		uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
		return reverse('password_reset_update_url', kwargs={'uidb64':uidb64,'token':token}), token, uidb64

	@staticmethod
	def generate_invalid_link_token_uid(user):
		#first generate valid link for user
		link,token,uid = ResetPasswordUpdate_Test.generate_valid_link_token_uid(user)
		#now change the user password to make the previously generated link now as invalid
		user.set_password('test789')	#dont use password attribute of user model directly as it will not generate hash of this password
		#set_password does not save the user object
		user.save()
		#now the link is invalid
		return link,token,uid 
		#the reason why we dont need refresh_from_db here because we have change password by user object itself not through some web page

	def test_1(self):
		response = self.client.get(self.valid_link,follow=True)
		self.assertEqual(response.status_code,200)	#302 because it get redirected to new link to hide token but because of follow final target code is 200
		self.assertEqual(self.resolveresult.url_name, 'password_reset_update_url')
		self.assertEqual(self.resolveresult.func.__name__,PasswordResetConfirmView.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.valid_link,follow=True)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(response.context.get('request').path))	#current path

	def test_3(self):
		response = self.client.get(self.valid_link,follow=True)
		self.assertContains(response, 'href="{}"'.format(self.loginurl))

	def test_4(self):
		response = self.client.get(self.invalid_link,follow=True)
		self.assertContains(response, 'you have clicked on invalid link')
		#can also check for 'validlink' in context sent by django internally as in docs

	def test_5(self):
		response = self.client.get(self.invalid_link,follow=True)
		self.assertContains(response, self.resetpasswordurl)

	def test_6(self):
		response = self.client.get(self.valid_link,follow=True)
		self.assertIsInstance(response.context.get('form'), SetPasswordForm)

	def test_7(self):
		response = self.client.get(self.valid_link,follow=True)
		response_formfields_seq = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_formfields_seq, self.formfields_seq)

	def test_8(self):
		response = self.client.get(self.valid_link,follow=True)
		self.assertContains(response, '<input type=', 3)	#csrf new_password1 new_password2
		self.assertContains(response, 'type="password"', 2)	#new_password1 new_password2

	def test_9(self):
		response = self.client.get(self.valid_link,follow=True)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_10(self):
		##below will not work - context-form data passed to link with token. but link is changed (w/o token link). so context for 2nd link is empty. so it will be treated as 
		#response = self.client.post(self.valid_link, data=self.resetpassworddata_correct, follow=True)
		#so we will first get the second link
		response = self.client.get(self.valid_link)
		#second link (w/o token) = response.url	#for follow=False(httpresponseredirect ) or response.context.get('request').path (templateresponse) for follow=True
		#now pass data to this link
		response = self.client.post(response.url, data=self.resetpassworddata_correct, follow=True)
		#check redirection
		self.assertRedirects(response=response, expected_url=self.resetpassworddoneurl, status_code=302, target_status_code=200)
		#check password change
		##since user1 password changed from web page not through user object, use db refresh
		self.user1.refresh_from_db()
		self.assertTrue(self.user1.check_password('mynametestabc1'))	#newpassword

	def test_11(self):
		#see explanation of test 10
		#since setuptestdata running for all test methods (maybe due to lack of transactional support), previous used link is valid now as it is created again
		response = self.client.get(self.valid_link)	#no follow so httpresponseredirect object
		response = self.client.post(response.url, data={})	#no follow
		self.assertEqual(response.status_code,200)	#not 302 redirection to reset done page

