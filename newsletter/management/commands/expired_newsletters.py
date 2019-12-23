from django.core.management.base import BaseCommand
from django.utils import timezone



# scripts

def expired_newsletter():
	print('list of expired newsletters.')




class Command(BaseCommand):
	help = 'clear expired newsletters in db.'
	# @use : python manage.py delete_users


	def handle(self,*args,**kwargs):
		expired_newsletter()
