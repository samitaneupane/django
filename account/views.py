from django.shortcuts import render,render_to_response,redirect
from django.contrib.auth.models import User
from account.forms import ( RegisterForm, LoginForm, 
							ChangePasswordForm, ProfileUpdateForm )
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import UserProfile
from myapp.models import myapp


def index(request):
    return render_to_response('index.html')
def login(request):
    return render_to_response('login.html')
    


# Create your views here.

def user_register(request):
	template_name = "register.html"
	form = RegisterForm

	if not request.method == "POST":
		return render(request, template_name, {'form': form})

	form = RegisterForm(request.POST)

	
	if not form.is_valid():
		return render(request, template_name, {'form': form})

	username = form.cleaned_data['username']
	email = form.cleaned_data['email']
	password = form.cleaned_data['password2']

	user = User()
	user.username = username
	user.email = email
	user.set_password(password)
	user.save()
	# Create user profile
	user_profile = UserProfile()
	user_profile.user = user
	user_profile.save()
	messages.success(request, "YOu have successfully registered.")

	return redirect("home")


def user_login(request):

	template_name = "login.html"
	form = LoginForm

	if not request.method == 'POST':
		return render(request, template_name, {'form': form})


	username = request.POST['username']
	password = request.POST['password']

	authenticated_user = authenticate(username=username, password=password)

	if not authenticated_user:
		messages.error(request, "Username or password mismatch")
		return render(request, template_name, {'form': form})

	login(request, authenticated_user)
	messages.success(request, "Logged in successfully")
	
	return redirect("home")


def user_logout(request):

	logout(request)

	return redirect("login")


def change_password(request):

	if not request.user.is_authenticated():
		messages.error(request, "You must log in to change your password")
		return redirect("login")

	template_name = "change_password.html"
	form = ChangePasswordForm

	if not request.method == "POST":
		return render(request, template_name, {'form': form})


	form = ChangePasswordForm(request.POST)

	if not form.is_valid():
		return render(request, template_name, {'form': form})


	old_password = form.cleaned_data['old_password']
	new_password = form.cleaned_data['new_password2']

	# user = User.objects.get(id=request.user.id)

	if not request.user.check_password(old_password):
		messages.error(request, "Your old password didn't match")
		return render(request, template_name, {'form': form})
		# raise ValidationError('Your old password didnt match')

	request.user.set_password(new_password)
	request.user.save()

	return redirect("home")


def profile(request, **kwargs):

	template_name = "profile.html"

	# try:
	# 	user = User.objects.get(id=kwargs['user_id'])
	# except Exception as e:
	# 	messages.error(request, e.message)
	# 	return redirect("home")

	try:
		user = User.objects.get(id=kwargs['user_id'])
	except ObjectDoesNotExist:
		messages.error(request, 'Sorry, this user is not in our database')
		return redirect("home")

	user_profile = UserProfile.objects.get(user=user)
	blogs = Blog.objects.filter(user=request.user)


	return render(request, template_name, {'user': user, 'user_profile': user_profile, 'blogs': blogs})


def profile_update(request, **kwargs):

	if not request.user.is_authenticated():
		messages.error(request, "You must login to edit your profile")
		return redirect("login")
		
	template_name = "profile_update.html"

	try:
		user = User.objects.get(id=kwargs['user_id'])
	except ObjectDoesNotExist:
		messages.error(request, 'Sorry, this user is not in our database')
		return redirect("home")

	user_profile = UserProfile.objects.get(user=user)

	form = ProfileUpdateForm(instance=user_profile)

	if not request.method == "POST":
		return render(request, template_name, {'form': form})

	form = ProfileUpdateForm(request.POST, request.FILES,  instance=user_profile)

	if not form.is_valid():
		return render(request, template_name, {'form': form})

	user_profile.full_name = form.cleaned_data['full_name']
	user_profile.address = form.cleaned_data['address']
	user_profile.phone = form.cleaned_data['phone']
	user_profile.avatar = form.cleaned_data['avatar']
	user_profile.save()

	return redirect("profile", user.id)


