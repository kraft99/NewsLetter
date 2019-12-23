import uuid
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text

def activation_token():
	token_ = str(uuid.uuid4()).replace('-','')
	return urlsafe_base64_encode(force_bytes(token_))



'''
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text

mssg = 'hello universe'

encode_mssg = urlsafe_base64_encode(force_bytes(mssg))

`aGVsbG8gdW5pdmVyc2U` 


decode_mssg = force_text(urlsafe_base64_decode(encode_mssg))

`hello universe`

'''


