from django.core.management.base import BaseCommand
from django.utils import timezone



# scripts

def clear_expired_newsletter():
	print('cleared expired newsletters.')




class Command(BaseCommand):
	help = 'clear expired newsletters in db.'
	# @use : python manage.py delete_users


	def handle(self,*args,**kwargs):
		clear_expired_newsletter()
