import os
import binascii
import urllib.request
import json
from passlib.hash import pbkdf2_sha256

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core import mail
from django.utils import timezone

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



@csrf_exempt
def social_auth(request, arg):

	json_resp = {}

	if arg not in ['vk']:
		json_resp['status'] = False
		json_resp['responseText'] = 'Social auth not supported for: %s' % arg
		return utility.default_response(json_resp, status=200)

	# ссылка для frontend части, для авторизации пользователя в социальной сети
	url_step_auth = 'https://oauth.vk.com/authorize/?response_type=code&client_id=%s&redirect_uri=%s,scope=email' % (settings.VK_CLIENT_ID, settings.VK_REDIRECT_URI)


	error_resp = request.GET.get('error', None)
	if error_resp:
		json_resp['status'] = False
		json_resp['responseText'] = error_resp + ': ' + request.GET.get('error_description', '')
		return utility.default_response(json_resp, status=200)

	code = request.GET.get('code', None)
	if code:

		# ссылка для получения токена доступа, user_id и email адреса
		url_step_token = 'https://oauth.vk.com/access_token?client_id=%s&client_secret=%s&code=%s&redirect_uri=%s' % (settings.VK_CLIENT_ID, settings.VK_CLIENT_SECRET, code, settings.VK_REDIRECT_URI)

		try:
			# получаем access_token, user_id и email
			data = urllib.request.urlopen(url_step_token).read().decode()
		except urllib.error.HTTPError as e:
			if str(e) == 'HTTP Error 401: Unauthorized':
				json_resp['status'] = False
				json_resp['responseText'] = 'Application Unauthorized with social driver'
				return utility.default_response(json_resp, status=200)

		data = json.loads(data)

		vk_user_id = str(data['user_id'])
		vk_email = data.get('email', '')
		vk_access_token = data['access_token']
		vk_expires_in = str(data['expires_in'])


		# используя полученный выше user_id и access_token, забираем данные пользователя
		fields = 'uid,first_name,last_name,screen_name,sex,bdate,photo_max_orig'
		url_step_user = 'https://api.vk.com/method/users.get?user_ids=%s&access_token=%s&fields=%s' % (vk_user_id, vk_access_token, fields)

		try:
			user_data = urllib.request.urlopen(url_step_user).read().decode()
		except Exception as e:
			json_resp['status'] = False
			json_resp['responseText'] = 'Failed fetching profile info: %s' % str(e)
			return utility.default_response(json_resp, status=200)

		user_data = json.loads(user_data)
		user_data = user_data['response'][0]


		### All data received ###
		### Authenticate or register social account user ###

		vk_account = AuthVk.objects.filter(vk_user_id=vk_user_id).first()
		client = Clients.objects.filter(vk_user_id=vk_user_id).first()

		if vk_account and client:

			# Update user information and Authenticate

			AuthVk.objects.filter(vk_user_id=vk_user_id).update(email=vk_email)
			AuthVk.objects.filter(vk_user_id=vk_user_id).update(access_token=vk_access_token)
			AuthVk.objects.filter(vk_user_id=vk_user_id).update(expires_in=vk_expires_in)
			AuthVk.objects.filter(vk_user_id=vk_user_id).update(profile=user_data)
			AuthVk.objects.filter(vk_user_id=vk_user_id).update(updated=timezone.now())


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
				AuthVk.objects.filter(vk_user_id=vk_user_id).delete()

			if client:
				json_resp['status'] = False
				json_resp['responseText'] = 'Social auth: failed to register new user. Client with such vk_user_id already exists'
				return utility.default_response(json_resp, status=200)

			client = Clients(
				vk_user_id = vk_user_id,
			)
			client.save()

			vk_account = AuthVk(
				vk_user_id = vk_user_id,
				email = vk_email,
				access_token = vk_access_token,
				expires_in = vk_expires_in,
				profile = user_data,
				updated = timezone.now(),
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
		json_resp['responseText'] = 'GET argument not defined: code'
		return utility.default_response(json_resp, status=200)