import json
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import StreamingHttpResponse, HttpResponseRedirect


def signin(request):

    json_resp = {}
    json_resp['status'] = True

    referer = request.META.get('HTTP_REFERER', '/')
    if 'auth' in referer or 'account' in referer:
        referer = '/'
    json_resp['redirectURL'] = referer if request.META['HTTP_HOST'] in referer else '/'

    if request.user.is_authenticated():
        json_resp['responseText'] = 'Already authenticated.'
    else:
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if email != '' and password != '':

            account = authenticate(email=email, password=password)
            if account is not None:
                if account.is_active:
                    login(request, account)
                    json_resp['responseText'] = 'Authenticated.'
                else:
                    json_resp['responseText'] = 'User is inactive, please activate account first.'
                    json_resp['redirectURL'] = ''
            else:
                json_resp['responseText'] = 'Incorrect username or password.'
                json_resp['redirectURL'] = ''
    return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json")


def signup(request):
    pass


def signout(request):

    # if not request.user.is_authenticated():
    #     return HttpResponseRedirect('/')

    # if request.method == "POST":
    #     logout(request)
    #     return HttpResponseRedirect(request.POST.get('referer', '/'))

    # referer = request.META.get('HTTP_REFERER', '/')

    # template = loader.get_template('auth/signout.html')
    # template_args = {
    #     'request': request,
    #     'title': 'Sign Out',
    #     'referer': referer if request.META['HTTP_HOST'] in referer else '/',
    # }
    # return StreamingHttpResponse(template.render(template_args, request))


def cabinet(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    template = loader.get_template('content.html')
    template_args = {
        'content': 'pages/cabinet.html',
        'request': request,
        'title': 'Кабинет',
    }
    return StreamingHttpResponse(template.render(template_args, request))