import os
import binascii
import json
from django.core import mail
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User

from ptpgo.models import Clients


def signin(request):

    json_resp = {}
    json_resp['status'] = True

    referer = request.META.get('HTTP_REFERER', '/')
    if 'auth' in referer or 'account' in referer:
        referer = '/'
    json_resp['redirectURL'] = referer if request.META['HTTP_HOST'] in referer else '/'

    if request.user.is_authenticated():
        print('here')
        return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json")


    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()

    if email and password:

        account = authenticate(email=email, password=password)
        if account is not None:
            if account.is_active:
                login(request, account)
                json_resp['responseText'] = ''
            else:
                json_resp['responseText'] = 'Пользователь неактивирован'
                json_resp['redirectURL'] = ''
        else:
            json_resp['responseText'] = 'Неверный email или пароль'
            json_resp['redirectURL'] = ''
    return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json")


def signup(request):

    json_resp = {}
    json_resp['status'] = True

    referer = request.META.get('HTTP_REFERER', '/')
    if 'auth' in referer or 'account' in referer:
        referer = '/'
    json_resp['redirectURL'] = referer if request.META['HTTP_HOST'] in referer else '/'

    if request.user.is_authenticated():
        return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json")


    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    password_verify = request.POST.get('password_verify', '').strip()

    if email and password and password_verify and password == password_verify:

        check_user = User.objects.filter(email=email).first()
        if check_user:
            json_resp['responseText'] = 'Пользователь с указанным email адресом уже существует'
            json_resp['redirectURL'] = ''
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password)
            client = Clients(
                user=user,
                email_confirmed=False,
                email_confirm_code=binascii.hexlify(os.urandom(25)).decode('utf-8'),
            )
            client.save()

            ##### SEND EMAIL WITH CONFIRMATION CODE #####
            connection = mail.get_connection()
            connection.open()

            subject = "Пожалуйста, подтвердите свой адрес электронной почты - PTPGO"
            body = """Добро пожаловать на PTPGO.\nЧтобы завершить регистрацию, вам необходимо подтвердить свой адрес электронной почты.\n
Подтвердить по ссылке: https://{0}/confirm_email/?confirm_code={1}\n
Спасибо,
Команда PTPGO\n""".format(request.META['HTTP_HOST'], client.email_confirm_code)

            email = mail.EmailMessage(subject, body, settings.SYSTEM_EMAIL_FROM,
                                  [email], connection=connection)

            email.send()
            connection.close()

    else:
        json_resp['responseText'] = 'Ошибка введенных данных'
        json_resp['redirectURL'] = ''

    return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json")


def confirm_email(request):

    confirm_code = request.GET.get('confirm_code', None)
    if not confirm_code:
        HttpResponseRedirect('/')

    client = Clients.objects.filter(email_confirm_code=confirm_code).first()
    if not client:
        HttpResponseRedirect('/')

    Clients.objects.filter(id=client.id).update(email_confirm_code="")
    Clients.objects.filter(id=client.id).update(email_confirmed=True)

    email_confirmed = True

    template = loader.get_template('content.html')
    template_args = {
        'content': 'pages/client/confirm_email.html'
        'request': request,
        'title': 'Подтверждение E-Mail адреса',
        'header_class': 'undefined',
        'email_confirmed': email_confirmed,
    }
    return StreamingHttpResponse(template.render(template_args, request))


def signout(request):
    pass
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
        'content': 'pages/client/cabinet.html',
        'request': request,
        'title': 'Кабинет',
        'header_class': 'undefined',
    }
    return StreamingHttpResponse(template.render(template_args, request))