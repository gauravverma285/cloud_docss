from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
gender = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
status=[('Active','Active'),('Inactive','Inactive'),('Delete','Delete'),]

class User(AbstractUser):
	name = models.CharField(max_length=160, null=True, blank=True)
	email = models.EmailField(blank=False, unique=True)
	mobile = models.CharField(max_length=15, null=True, blank=True)
	gender = models.CharField(max_length=10, choices=gender, default='Male') 
	dob = models.DateField(null=True, blank=True)
	otp = models.CharField(max_length=10, null=True, blank=True)
	is_verified = models.BooleanField(default=False)
	created_time = models.DateTimeField(auto_now_add=True)
	utimestamp = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
	track = models.TextField(blank=True, editable=False)
	utrack = models.TextField(blank=True, editable=False)
	status = models.CharField(max_length=20, choices=status, default='Active')


	def __str__(self):
		return self.username 
	

class Client(models.Model):
	name = models.CharField(max_length=160, null=True, blank=True)
	email = models.EmailField(blank=False, unique=True)
	mobile = models.CharField(max_length=15, null=True, blank=True)
	utimestamp = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
	track = models.TextField(blank=True, editable=False)
	utrack = models.TextField(blank=True, editable=False)
	status = models.CharField(max_length=20, choices=status, default='Active')

	def __str__(self):
		return self.email
	

class ClientDocument(models.Model):
	client = models.ForeignKey( Client, on_delete = models.CASCADE)
	document = models.FileField(upload_to = 'clientdocument/')
	utimestamp = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True ,null=True, blank=True)
	track = models.TextField(blank=True, editable=False)
	utrack = models.TextField(blank=True, editable=False)
	status = models.CharField(max_length=20, choices=status, default='Active')


	def __str__(self):
		return self.client
	
	