import os
import binascii
from passlib.hash import pbkdf2_sha256

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core import mail

from ptpgo.models import Clients, Tokens, AuthVk
from ptpgo.functions import utility



@csrf_exempt
def authenticate(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'POST':
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)

		facebook_id = request.POST.get('facebook_id', None)
		google_plus_id = request.POST.get('google_plus_id', None)
		vk_id = request.POST.get('vk_id', None)

		if email and password:

			hash_password = pbkdf2_sha256.encrypt(password, rounds=10, salt_size=0)

			client = Clients.objects.filter(email=email, password=hash_password).first()
			if client:

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
			else:
				json_resp['status'] = False
				json_resp['responseText'] = 'incorrect authentication data'
				return utility.default_response(json_resp, 200)

		elif vk_id:

			vk_account = AuthVk.objects.filter(vk_id=vk_id).first()
			client = Clients.objects.filter(vk_id=vk_id).first()

			if vk_account and client:

				# Authenticate

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

			else:

				# Register new user

				if vk_account:
					AuthVk.objects.filter(vk_id=vk_id).delete()

				if client:
					json_resp['status'] = False
					json_resp['responseText'] = 'Social auth: failed to register new user. Client with such vk_id already exists'
					return utility.default_response(json_resp, status=200)

				client = Clients(
					vk_id = vk_id,
				)
				client.save()

				vk_account = AuthVk(
					vk_id = vk_id,
				)
				vk_account.save()

				# Authenticate
				token = Tokens(
					client = client,
					token = binascii.hexlify(os.urandom(25)).decode('utf-8'),
				)
				token.save()

				json_resp['status'] = True
				json_resp['response'] = {
					'token': token.token,
				}
				json_resp['responseText'] = 'Social auth (vk): registered new user. Use provided token to keep session active'
				return utility.default_response(json_resp, status=201)

		else:
			json_resp['status'] = False
			json_resp['responseText'] = 'incorrect fields'
			return utility.default_response(json_resp, status=200)

	else:
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use POST with client authentication credentials' % request.method
		return utility.default_response(json_resp, 405)



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
def register_with_email(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'POST':

		email = request.POST.get('email', None)
		password = request.POST.get('password', None)
		first_name = request.POST.get('first_name', '')
		last_name = request.POST.get('last_name', '')

		if email and password and first_name and last_name:

			try:
				validate_email(email)
			except ValidationError as e:
				json_resp['status'] = False
				json_resp['responseText'] = 'Email format invalid: %s' % str(e)
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
				first_name = first_name,
				last_name = last_name,
				email_confirm_code = binascii.hexlify(os.urandom(25)).decode('utf-8'),
			)
			client.save()


			##### SEND EMAIL WITH CONFIRMATION CODE #####
			connection = mail.get_connection()
			connection.open()

			subject = "Пожалуйста, подтвердите свой адрес электронной почты"
			body = """Здравствуйте, {0}!\n\nДобро пожаловать на ptpgo.\nЧтобы завершить регистрацию, вам необходимо подтвердить свой адрес электронной почты.\n
Подтвердить по ссылке: https://ptpgo.ru/confirm_email/?confirm_code={1}\n
Спасибо,
Команда ptpgo\n""".format(client.first_name, client.email_confirm_code)

			email = mail.EmailMessage(subject, body, settings.SYSTEM_EMAIL_FROM,
								  [email], connection=connection)

			email.send()
			connection.close()


			# Authenticate
			token = Tokens(
				client = client,
				token = binascii.hexlify(os.urandom(25)).decode('utf-8'),
			)
			token.save()


			json_resp['status'] = True
			json_resp['response'] = {
				'token': token.token,
			}
			json_resp['responseText'] = 'Registered. Sent email confirmation. Use provided token to keep session active'
			return utility.default_response(json_resp, status=201)

		json_resp['status'] = False
		json_resp['responseText'] = 'some fields are incorrect: email, password, first_name, last_name'
		return utility.default_response(json_resp, status=200)

	else:
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use POST with fields: email, password, first_name, last_name' % request.method
		return utility.default_response(json_resp, status=405)



@csrf_exempt
def confirm_email(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	if request.method == 'POST':
		confirm_code = request.POST.get('confirm_code', None)

		if confirm_code:
			client = Clients.objects.filter(email_confirm_code=confirm_code).first()
			if client:
				Clients.objects.filter(id=client.id).update(email_confirm_code="")
				Clients.objects.filter(id=client.id).update(email_confirmed=True)

				json_resp['status'] = True
				json_resp['responseText'] = 'Email confirmed'
				return utility.default_response(json_resp, status=200)

			json_resp['status'] = False
			json_resp['responseText'] = 'Client with such email_confirm_code not found'
			return utility.default_response(json_resp, status=200)

		json_resp['status'] = False
		json_resp['responseText'] = 'incorrect confirm_code field'
		return utility.default_response(json_resp, status=200)

	else:
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use POST with fields: confirm_code' % request.method
		return utility.default_response(json_resp, status=405)

