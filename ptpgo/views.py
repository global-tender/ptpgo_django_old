import os
import json
import binascii
from passlib.hash import pbkdf2_sha256

from django.conf import settings

from django.http import StreamingHttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core import mail

from ptpgo.models import Clients, Tokens, ClientPhotos, ClientRatings
from ptpgo.utility import utility


def home(request):
	return HttpResponseRedirect('/rest/')



@csrf_exempt
def rest_home(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'GET':
		status = 200
		json_resp['status'] = True
		json_resp['responseText'] = 'List of API methods'

		json_resp['response'] = {
			'authenticate': 'https://' + request.META['HTTP_HOST'] + '/authenticate/',
			'check_auth': 'https://' + request.META['HTTP_HOST'] + '/check_auth/',
			'register': 'https://' + request.META['HTTP_HOST'] + '/register/',
			'confirm_register': 'https://' + request.META['HTTP_HOST'] + '/confirm_register/',
		}

	else:
		status = 405
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed' % request.method

	return utility.default_response(json_resp, status)



@csrf_exempt
def authenticate(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'GET':
		status = 405
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use POST with client authentication credentials' % request.method
	elif request.method == 'POST':
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)

		if email and password:

			hash_password = pbkdf2_sha256.encrypt(password, rounds=10, salt_size=0)

			client = Clients.objects.filter(email=email, password=hash_password).first()
			if client:

				if client.confirm_code:
					json_resp['status'] = False
					json_resp['responseText'] = 'Account is not confirmed. Authentication failed'
					return utility.default_response(json_resp, status=200)

				token = Tokens(
					client = client,
					token = binascii.hexlify(os.urandom(25)).decode('utf-8'),
				)
				token.save()

				json_resp['status'] = True
				json_resp['response'] = {
					'token': token.token,
				}
				json_resp['responseText'] = 'Authenticated. Use provided token to keep session active'
				return utility.default_response(json_resp, status=201)

		status = 200
		json_resp['status'] = False
		json_resp['responseText'] = 'incorrect email or password'

	return utility.default_response(json_resp, status)



@csrf_exempt
def check_auth(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'GET':
		request_token = request.GET.get('token', None)

		if request_token:
			token = Tokens.objects.filter(token=request_token).first()
			if token:
				json_resp['status'] = True
				json_resp['responseText'] = 'Token found. Client is authenticated'
				return utility.default_response(json_resp, status=200)

		json_resp['status'] = False
		json_resp['responseText'] = 'Token not found. Client is not authenticated'
		return utility.default_response(json_resp, status=200)
	else:
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use GET with field: token' % request.method
		return utility.default_response(json_resp, status=405)

@csrf_exempt
def register(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'POST':

		email = request.POST.get('email', None)
		password = request.POST.get('password', None)

		if email and password:

			try:
				validate_email(email)
			except ValidationError as e:
				json_resp['status'] = False
				json_resp['responseText'] = 'Email format invalid'
				return utility.default_response(json_resp, status=200)

			client_exists = Clients.objects.filter(email=email).first()
			if client_exists:
				json_resp['status'] = False
				json_resp['responseText'] = 'Client with such email address already registered'
				return utility.default_response(json_resp, status=200)

			if len(password) < 6:
				json_resp['status'] = False
				json_resp['responseText'] = 'Password length is less than 6 chars'
				return utility.default_response(json_resp, status=200)

			hash_password = pbkdf2_sha256.encrypt(password, rounds=10, salt_size=0)

			client = Clients(
				email = email,
				password = hash_password,
				confirm_code = binascii.hexlify(os.urandom(25)).decode('utf-8'),
			)
			client.save()


			##### SEND EMAIL WITH CONFIRMATION CODE #####
			connection = mail.get_connection()
			connection.open()

			subject = "Подтверждение регистрации"
			body = """Для завершения регистрации пройдите по следующей ссылке: https://ptpgo.com/confirm_account/?confirm_code={0}
			""".format(client.confirm_code)

			email = mail.EmailMessage(subject, body, settings.SYSTEM_EMAIL_FROM,
								  [email], connection=connection)

			email.send()
			connection.close()

			json_resp['status'] = True
			json_resp['responseText'] = 'Registered. Confirmation is required'
			return utility.default_response(json_resp, status=200)

		json_resp['status'] = False
		json_resp['responseText'] = 'incorrect email or password fields'
		return utility.default_response(json_resp, status=200)

	else:
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use POST with fields: email, password' % request.method
		return utility.default_response(json_resp, status=405)



@csrf_exempt
def confirm_register(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'POST':
		confirm_code = request.POST.get('confirm_code', None)

		if confirm_code:
			client = Clients.objects.filter(confirm_code=confirm_code).first()
			if client:
				Clients.objects.filter(confirm_code=confirm_code).update(confirm_code="")

				json_resp['status'] = True
				json_resp['responseText'] = 'Registration confirmed'
				return utility.default_response(json_resp, status=200)

			json_resp['status'] = False
			json_resp['responseText'] = 'Client with such confirm_code not found'
			return utility.default_response(json_resp, status=200)

		json_resp['status'] = False
		json_resp['responseText'] = 'incorrect confirm_code field'
		return utility.default_response(json_resp, status=200)

	else:
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use POST with fields: confirm_code' % request.method
		return utility.default_response(json_resp, status=405)

