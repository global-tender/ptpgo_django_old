from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from ptpgo.functions import utility



def index(request):
	return HttpResponseRedirect('/rest/')



@csrf_exempt
def rest_index(request):

	if not utility.is_rest_user(request):
		return utility.rest_unauthorized()

	json_resp = {}

	status = 200
	json_resp['status'] = True
	json_resp['responseText'] = 'List of API methods'

	json_resp['response'] = {
		'authenticate': 'https://' + request.META['HTTP_HOST'] + '/rest/authenticate/',
		'check_auth': 'https://' + request.META['HTTP_HOST'] + '/rest/check_auth/',
		'register_with_email': 'https://' + request.META['HTTP_HOST'] + '/rest/register_with_email/',
		'confirm_email': 'https://' + request.META['HTTP_HOST'] + '/rest/confirm_email/',
	}

	return utility.default_response(json_resp, status)

