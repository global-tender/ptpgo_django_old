from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import StreamingHttpResponse, HttpResponseRedirect


def signout(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(request.POST.get('referer', '/'))

    referer = request.META.get('HTTP_REFERER', '/')

    template = loader.get_template('auth/signout.html')
    template_args = {
        'request': request,
        'title': 'Sign Out',
        'referer': referer if request.META['HTTP_HOST'] in referer else '/',
    }
    return StreamingHttpResponse(template.render(template_args, request))


def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    errors = []

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    remember = request.POST.get('remember', '')
    input_referer = request.POST.get('referer', '/')

    if email != '' and password != '':

        if not remember:
            request.session.set_expiry(0)  # the user’s session cookie will expire when the user’s Web browser is closed.

        account = authenticate(email=email, password=password)
        if account is not None:
            if account.is_active:
                login(request, account)
                return HttpResponseRedirect(input_referer)
            else:
                errors.append("User is inactive, please activate account first.")
        else:
            errors.append("Incorrect username or password.")

    referer = request.META.get('HTTP_REFERER', '/')
    if input_referer != '/':
        referer = input_referer
    if 'auth' in referer or 'account' in referer:
        referer = '/'

    template = loader.get_template('auth/signin.html')
    template_args = {
        'request': request,
        'title': 'Sign In',
        'referer': referer if request.META['HTTP_HOST'] in referer else '/',
        'errors': errors,
    }
    return StreamingHttpResponse(template.render(template_args, request))