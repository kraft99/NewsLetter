import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .utils import date_duration
from .token import activation_token

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError,send_mail
from django.template.loader import render_to_string
from django.db import models



class NewsLetter(models.Model):
	''' NewsLetter Model.
	
	@@attr. 

	email 			- Email 
	ip 	  			- Ip Address
	is_subscribed  	- DateTime (indicate whether subscription is confirmed)
	@@methods.
	
	 '''
	email 					= models.EmailField(max_length=170)
	ip     					= models.GenericIPAddressField()
	is_subscribed			= models.DateTimeField(blank=True,null=True) # new

	created 				= models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering 			= ('-created',)
		verbose_name 		= 'NewsLetter'
		verbose_name_plural = 'NewsLetters'


	def __str__(self):
		return self.email


	@classmethod
	def unconfirmed_newsletters(cls):
		return cls.objects.filter(is_subscribed__isnull=True)


# Exceptions
class ActivationError(Exception):pass
class ActivationCodeExistError(Exception):pass

class Activation(models.Model):
	'''Activation Model'''
	token 					= models.CharField(max_length=250,blank=True,null=True,unique=True,editable=False)
	newsletter 				= models.OneToOneField(to=NewsLetter,on_delete=models.CASCADE) 
	expired 				= models.DateTimeField(blank=True,null=True)
	is_sent 				= models.BooleanField(default=False)

	created 				= models.DateTimeField(auto_now_add=True)


	class Meta:
		ordering 	= ('-created',)
		verbose_name = 'Activation'
		verbose_name_plural = 'Activations'


	def __str__(self):
		return str(self.newsletter.email)

	def save(self,*args,**kwargs):
		super(Activation,self).save(*args,**kwargs)
		



	def send(self,request=None):
		'''
		TODO:
		1. Send Email via SendGrid & MailChimp (learning purposes)
		2. Find a Better Way to generate validation link - DONT HARD CORD IT !
		'''
		domain  = get_current_site(request).domain
		link_url = 'http://{0}/token-validation/auth/{1}/'.format(domain,self.token)
		message = "{1} to confirm subscription".format(domain,link_url)
		try:
			send_mail('Confirm Subscription', message, 'noreply@kraft99.co', [self.newsletter.email])
		except BadHeaderError:
			pass
		



	@classmethod
	def create_activation(cls,instance):
		return cls.objects.create(token = activation_token(),
							newsletter = instance,
							expired=date_duration(),
							is_sent=True)



	def has_expired(self):
		return timezone.now() > self.expired

	has_expired = property(has_expired)


