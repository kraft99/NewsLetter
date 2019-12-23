from .models import NewsLetter
from django import forms


class SubscribeForm(forms.ModelForm):
	email 	   = forms.EmailField(label='',required=True,help_text='kindly hit ENTER when you fill input.',widget=forms.EmailInput())
	class Meta:
		model  = NewsLetter
		fields = ('email',)

	def __init__(self,*args,**kwargs):
		super(SubscribeForm,self).__init__(*args,**kwargs)
		self.fields['email'].widget.attrs.update({'placeholder':'eg.edward@bimmeo.com'})


