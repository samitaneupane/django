from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from account.models import UserProfile

class RegisterForm(forms.Form):

	username = forms.CharField(label="Username", max_length=30)
	email = forms.EmailField()
	password1 = forms.CharField(widget=forms.PasswordInput,label='Password', max_length=30 )
	password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput , max_length=30)

	def clean_username(self):

		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise ValidationError("This username is already taken")

		return username

	def clean_password2(self):

		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']

		if password1 and password2 and password1 != password2:
			raise ValidationError("Sorry your password didn't match")

		if len(password2) < 8:
			raise ValidationError("Password must be 8 characters in length")

		return password2


class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.PasswordInput,label="Username", max_length=30)
	password = forms.CharField(widget=forms.PasswordInput,label="password", max_length=30)


class ChangePasswordForm(forms.Form):

	old_password = forms.CharField(max_length=30)
	new_password1 = forms.CharField(max_length=30)
	new_password2 = forms.CharField(max_length=30)

	def clean_new_password2(self):

		new_password1 = self.cleaned_data['new_password1']
		new_password2 = self.cleaned_data['new_password2']

		if new_password1 and new_password2 and new_password1 != new_password2:
			raise ValidationError("Sorry your password didn't match")

		if len(new_password2) < 8:
			raise ValidationError("Password must be 8 characters in length")

		return new_password2


class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('full_name', 'address', 'phone', 'avatar')

