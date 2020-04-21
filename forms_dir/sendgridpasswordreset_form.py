from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.template.loader import render_to_string

UserModel = get_user_model()

#extend PasswordResetForm class
class SendgridPasswordReset_Form(PasswordResetForm):
	#override the save() method
	#copy the same method as it is & commented send_mail and added sendgrid sending method
	def save(self, domain_override=None,
   	         subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
		"""
		Generate a one-use only link for resetting password and send it to the
		user.
		"""
		email = self.cleaned_data["email"]
		email_field_name = UserModel.get_email_field_name()
		#below for loop will not be required as it will run only once but keeping it for code issues
		for user in self.get_users(email):
			if not domain_override:
				current_site = get_current_site(request)
				site_name = current_site.name
				domain = current_site.domain
			else:
				site_name = domain = domain_override
			user_email = getattr(user, email_field_name)
			context = {
                'email': user_email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
			}
			"""	#Commented the send_mail method
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                user_email, html_email_template_name=html_email_template_name,
            )
			"""
			#using the sendgrid email sending code
			#https://app.sendgrid.com/guide/integrate/langs/python
			email_message = Mail(
					#since this is api call, settings.default_from_email will not be used..also default_from_email should be string
					from_email = settings.DEFAULT_FROM_EMAIL,	
					to_emails = user_email,	#comma because this is tuple
					#since this is using api call, email_subject_prefix will not be used..so add it here
					subject = render_to_string(template_name='passwordresetsubject.txt'),
					html_content = render_to_string(template_name='passwordresetemailtemplate.html', context=context)
				)
			try:
				sendgrid_client = SendGridAPIClient(settings.SENDGRID_API_KEY)
				sendgrid_client.send(email_message)
			except Exception as e:
				print(e.message)