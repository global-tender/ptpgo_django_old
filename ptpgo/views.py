import json

from django.http import StreamingHttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt

from ptpgo.models import Clients, Tokens, ClientPhotos, ClientRatings, Country, City
from ptpgo.utility import utility


def home(request):
	return HttpResponseRedirect('/rest/')


@csrf_exempt
def rest_home(request):

	json_resp = {}

	if not utility.is_rest_user(request):
		status = 403
		json_resp['status'] = False
		json_resp['responseText'] = 'Forbidden, authentication is required.'
		return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)

	if request.method == 'GET':
		status = 200
		json_resp['status'] = True
		json_resp['responseText'] = 'List of API methods'

		json_resp['response'] = {
			'authenticate': 'https://' + request.META['HTTP_HOST'] + '/authenticate/',
		}

	else:
		status = 405
		json_resp['status'] = False
		json_resp['responseText'] = 'Method %s Not Allowed' % request.method

	return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)
