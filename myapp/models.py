from __future__ import unicode_literals

from django.db import models




from django.utils import timezone
from django.contrib.auth.models import User


class myapp(models.Model):

	user = models.ForeignKey(User, blank=True, null=True,on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	body = models.TextField()
	published_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.title