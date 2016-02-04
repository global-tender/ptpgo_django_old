
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