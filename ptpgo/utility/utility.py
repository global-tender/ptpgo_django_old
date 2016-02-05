import json
from django.http import StreamingHttpResponse
from django.conf import settings

def is_rest_user(request):
	if request.method == 'GET':
		rest_token = request.GET.get('rest_token', None)
	else:
		rest_token = request.POST.get('rest_token', None)

	if rest_token:
		if rest_token == settings.REST_TOKEN:
			return True

	return False

def rest_unauthorized():
	json_resp = {}
	status = 403
	json_resp['status'] = False
	json_resp['responseText'] = 'Forbidden, authentication is required.'
	return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json", status=status)