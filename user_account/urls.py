from django.urls import path
import user_account.views
from django.contrib.auth import views as django_auth_views
from django.urls import reverse_lazy

urlpatterns = [
	path('signup/', user_account.views.signupuser, name='signup_url'),
	path('logout/', django_auth_views.LogoutView.as_view(), name='logout_url'),
	path('login/', django_auth_views.LoginView.as_view(template_name='loginpage.html'), name='login_url'),
	path('changepassword/', django_auth_views.PasswordChangeView.as_view(
					template_name='passwordchangepage.html', 
					success_url=reverse_lazy('password_change_done_url')), name='password_change_url'),
    path('changepassword/done/', django_auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangepagedone.html'), name='password_change_done_url'),
    path('passwordreset/', user_account.views.NewPasswordReset_View.as_view(), name='password_reset_url'),	#enter email to get reset link
    path('passwordreset/sent/', django_auth_views.PasswordResetDoneView.as_view(template_name='passwordresetsentpage.html'), name='password_reset_sent_url'),	#ack that reset link sent to email
    path('passwordreset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(
    				template_name='passwordresetupdatepage.html',
    				success_url=reverse_lazy('password_reset_done_url')), name='password_reset_update_url'),	#form displayed to enter new password. URL pattern obtained from django\contrib\auth\urls.py
    path('passwordreset/done/', django_auth_views.PasswordResetCompleteView.as_view(template_name='passwordresetdonepage.html'), name='password_reset_done_url'),	#confirmation page that password is changed
    path('myprofile/update/', user_account.views.MyProfileUpdate_View.as_view(), name='myprofile_update_url'),  #url to update account profile    
]


