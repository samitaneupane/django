
from __future__ import unicode_literals
from django.db import models


from django.contrib.auth.models import User



class UserProfile(models.Model):

	user = models.ForeignKey(User,on_delete=models.CASCADE)
	full_name = models.CharField(max_length=100, blank=True, null=True)
	address = models.CharField(max_length=100, blank=True, null=True)
	phone = models.CharField(max_length=100, blank=True, null=True)
	avatar = models.FileField(upload_to='avatar', default='default.jpg')

	def __unicode__(self):
		return self.user.username

