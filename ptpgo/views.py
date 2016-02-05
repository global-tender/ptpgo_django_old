import os
import json
import binascii

from django.http import StreamingHttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from ptpgo.models import Clients, Tokens, ClientPhotos, ClientRatings, Country, City
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
		}

	else:
		status = 405
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed' % request.method

	return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)

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
			client = Clients.objects.filter(email=email, password=password).first()
			if client:

				token = Tokens(
					client = client,
					token = binascii.hexlify(os.urandom(25)).decode('utf-8'),
				)
				token.save()

				status = 201
				json_resp['status'] = True
				json_resp['response'] = {
					'token': token.token,
				}
				json_resp['responseText'] = 'Authenticated. Use provided token to keep session active'
				return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)

		status = 200
		json_resp['status'] = False
		json_resp['responseText'] = 'incorrect email or password'

	return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)


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
				status = 200
				json_resp['status'] = True
				json_resp['responseText'] = 'Token found. Client is authenticated'
				return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)

		status = 200
		json_resp['status'] = False
		json_resp['responseText'] = 'Token not found. Client is not authenticated'
		return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)
	else:
		status = 405
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed. Use GET with field: token' % request.method
		return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)

