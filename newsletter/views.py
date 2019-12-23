from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse,Http404
from django.shortcuts import redirect,get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse

from .models import NewsLetter,Activation
from .utils import visitor_ip_address
from .decorators import ajax_required
from .forms import SubscribeForm



def index(request):
	# index view renders form
	form = SubscribeForm()
	return TemplateResponse(request,'newsletter/subscribe.html',{'form':form})



def thank_you(request,**kwargs):
	''' renders a page with a message `THANK YOU ` '''
	return TemplateResponse(request,'newsletter/thank_you.html',{})




@ajax_required
@require_http_methods(["POST"])
def subscribe(request):
	# subscribe view handles submittion
	email = request.POST.get('content').strip()
	ip = visitor_ip_address(request)
	newsletter,created = NewsLetter.objects.get_or_create(email = email,ip=ip)
	if created:
		Activation.create_activation(newsletter).send(request)
	return JsonResponse({'data':created})



@require_http_methods(["POST"])
def unsubscribe(request):
	'''
	@approah
	use same processes for subscription.
	'''
	pass




@require_http_methods(["POST"])
@ajax_required
def validate_email(request):
	# validates email on KeyUp (ClientSide Js)
	email = request.POST.get('content').strip()
	is_taken = NewsLetter.objects.filter(email__iexact=email).exists()
	data = {'data':is_taken}
	return JsonResponse(data)




def validate_confirmation_token(request,token = None):
	# validate token after user clicks link to this place
	# after successful validation redirect user to thank you view with the token passed

	activation_obj = get_object_or_404(Activation,token__iexact=token,is_sent=True)
	# newsletter = get_object_or_404(Activation,token__iexact=token).newsletter
	if activation_obj.has_expired:
		return HttpResponse('Activation code is invalid.')
	else:
		from django.utils import timezone
		activation_obj.newsletter.is_subscribed = timezone.now()
		activation_obj.newsletter.save()
		activation_obj.delete() # remove activation object from db
		return redirect(reverse('newsletter:thank-you',kwargs={'token':activation_obj.token}))


