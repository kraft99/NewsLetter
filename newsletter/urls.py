from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('', views.index,name='index'),
    path('subscibe/',views.subscribe,name='subscribe'),
    path('unsubscribe/',views.unsubscribe,name='unsubscribe'),
    path('validate/',views.validate_email,name='validate-email'),

    # handles Token Validation
    # use confirm-subscription/auth/<str:token>/ instead of token-validation/auth/<str:token>/
    path('token-validation/auth/<str:token>/',views.validate_confirmation_token,name='validate-token'),
    path('thank-you/<str:token>/',views.thank_you,name='thank-you'),
]
