from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from user_account.views import MyProfileUpdate_View
from forms_dir.myprofileupdate_form import MyProfileUpdate_Form

class MyProfileUpdatePage_Test(TestCase):

	"""
	1. url status code, url_name and fucntion resolving
	2. link to home page, profile update page in navigation bar
	3. form csrf check
	4. form class check
	5. form fields sequence check
	6. form fields type and number check
	7. invalid data post - same page, no data updated
	8. empty fields data - same page, no data updated
	9. correct data - redirection and data updated
	"""

	@classmethod
	def setUpTestData(cls):
		cls.user = User.objects.create_user(username='test', email='test@test.com', password='test123')
		cls.profilepageurl = reverse('myprofile_update_url')
		cls.profilepagepath = '/user/myprofile/update/'
		cls.resolveresult = resolve(cls.profilepagepath)
		cls.homeurl = reverse('home_url')
		cls.formfields_seq = ['first_name', 'last_name', 'email']
		cls.profilepagedata_correct = {'first_name':'First', 'last_name':'Last', 'email':'email@test.com'}

	#login needed to access this page
	def setUp(self):
		self.client.login(username='test', password='test123')

	def test_1(self):
		response = self.client.get(self.profilepageurl)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(self.resolveresult.url_name, 'myprofile_update_url')
		self.assertEqual(self.resolveresult.func.__name__, MyProfileUpdate_View.as_view().__name__)

	def test_2(self):
		response = self.client.get(self.profilepageurl)
		self.assertContains(response, 'href="{}"'.format(self.homeurl))
		self.assertContains(response, 'href="{}"'.format(self.profilepageurl))

	def test_3(self):
		response = self.client.get(self.profilepageurl)
		self.assertContains(response, 'csrfmiddlewaretoken')

	def test_4(self):
		response = self.client.get(self.profilepageurl)
		self.assertIsInstance(response.context.get('form'), MyProfileUpdate_Form)

	def test_5(self):
		response = self.client.get(self.profilepageurl)
		response_formfields_seq = list(response.context.get('form').fields.keys())
		self.assertSequenceEqual(response_formfields_seq, self.formfields_seq)

	def test_6(self):
		response = self.client.get(self.profilepageurl)
		self.assertContains(response, '<input type=', 4)	#csrf first_name last_name email
		self.assertContains(response, 'type="text"', 2)	#first_name last_name
		self.assertContains(response, 'type="email"', 1)	#email

	def test_7(self):
		response = self.client.post(self.profilepageurl, data={})	#no follow
		self.assertEqual(response.status_code, 200)	#no 302 redirection
		#check if data not updated for user
		self.assertEqual(self.user.first_name, '')	
		self.assertEqual(self.user.last_name, '')
		self.assertEqual(self.user.email, 'test@test.com')

	def test_8(self):
		response = self.client.post(self.profilepageurl, data={'first_name':'', 'last_name':'', 'email':''})	#no follow
		self.assertEqual(response.status_code, 200)	#no 302 redirection
		#check if data not updated for user
		self.assertEqual(self.user.first_name, '')	
		self.assertEqual(self.user.last_name, '')
		self.assertEqual(self.user.email, 'test@test.com')

	def test_9(self):
		response = self.client.post(self.profilepageurl, data=self.profilepagedata_correct, follow=True)
		self.assertRedirects(response=response, expected_url=self.homeurl, status_code=302, target_status_code=200)
		#check if data not updated for user
		#since data updated by webpage , we will use refresh_from_db
		self.user.refresh_from_db()
		self.assertEqual(self.user.first_name, 'First')	
		self.assertEqual(self.user.last_name, 'Last')
		self.assertEqual(self.user.email, 'email@test.com')		
