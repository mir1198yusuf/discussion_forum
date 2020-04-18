from django.shortcuts import render, redirect
from forms_dir.signup_form import SignUp_Form
from forms_dir.myprofileupdate_form import MyProfileUpdate_Form
from django.contrib.auth import authenticate,login,logout
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.

#signup function
def signupuser(request):
	#check if user is logged in, if yes redirect to home page
	if not request.user.is_authenticated:	#if False means not logged in 
		if request.method=='POST':
			form = SignUp_Form(request.POST)	#create form with posted data
			if form.is_valid():
				form.save(commit=True)	#create the user
				#authenticate the user
				user =  authenticate(request, username=request.POST['username'], password=request.POST['password1'])
				#form fields are username,...., password1, password2
				if user:	#if not None value return from authenticate
					login(request,user)		#log in the user
					return redirect('home_url')	#redirect to home page
		elif request.method=='GET':	
			form = SignUp_Form()
		return render(request, 'signuppage.html', {'form':form})
	else:
		return redirect('home_url')	#redirect to home page

#my profile update CBV based on UpdateView GBCV
@method_decorator(login_required, name='dispatch')
class MyProfileUpdate_View(UpdateView):
	form_class = MyProfileUpdate_Form
	model = User 
	template_name = 'myprofileupdatepage.html'
	success_url = reverse_lazy('home_url')

	def get_object(self):
		return self.request.user

