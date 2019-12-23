# import datetime
# from dateutil.relativedelta import relativedelta
# from django.db.models.signals import post_save,pre_save
# from django.dispatch import receiver


# from .models import NewsLetter,Activation
# from .token import activation_token


# def date_duration(now = datetime.datetime.now()):
# 	return now + relativedelta(weeks = 1)
	


# @receiver(post_save,sender=NewsLetter)
# def create_activate(sender,instance,created,**kwargs):
# # @purpose : create a new activation object for newly created newsletter
#     if created:
#         Activation.objects.create(token = activation_token(),newsletter = instance,expired=date_duration(),is_sent=True)