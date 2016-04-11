import os
import binascii
import json
import random
import urllib.request
import urllib.parse
from django.core import mail
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings

from ptpgo.utility import utility
from ptpgo.models import Clients


def signin(request):

    if request.method == 'GET':
        return HttpResponseRedirect('/')

    json_resp = {}
    json_resp['status'] = True
    json_resp['redirectURL'] = utility.get_referer(request)

    if request.user.is_authenticated():
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

    if request.method == 'GET':
        return HttpResponseRedirect('/')

    json_resp = {}
    json_resp['status'] = True
    json_resp['redirectURL'] = utility.get_referer(request)

    if request.user.is_authenticated():
        return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json")

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    password_verify = request.POST.get('password_verify', '').strip()

    if email and password and password_verify and password == password_verify:

        check_user = User.objects.filter(email__exact=email).first()
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

            # Authenticate registered user
            user.backend = 'ptpgo.backends.CustomAuthBackend'
            login(request, user)
            json_resp['redirectURL'] = '/cabinet/'

    else:
        json_resp['responseText'] = 'Ошибка введенных данных'
        json_resp['redirectURL'] = ''

    return StreamingHttpResponse(json.dumps(json_resp, indent=4), content_type="application/vnd.api+json")


def confirm_email(request):

    email_confirmed = False

    confirm_code = request.GET.get('confirm_code', None)
    if not confirm_code:
        return HttpResponseRedirect('/')

    client = Clients.objects.filter(email_confirm_code=confirm_code).first()
    if client:
        Clients.objects.filter(id=client.id).update(email_confirm_code="")
        Clients.objects.filter(id=client.id).update(email_confirmed=True)

        email_confirmed = True
    else:
        return HttpResponseRedirect('/')

    template = loader.get_template('pages/client/confirm_email.html')
    template_args = {
        'request': request,
        'title': 'Подтверждение E-Mail адреса',
        'header_class': 'undefined',
        'email_confirmed': email_confirmed,
    }
    return StreamingHttpResponse(template.render(template_args, request))


def add_phone(request):

    referer = utility.get_referer(request)

    if not request.user.is_authenticated():
        return HttpResponseRedirect(referer)

    phone_confirmed = False
    added_phone = False

    client = Clients.objects.filter(user=request.user).first()
    if client:

        if client.phone:
            added_phone = client.phone

        if client.phone_confirmed:
            phone_confirmed = True

        if request.method == 'POST':
            phone = request.POST.get('phone', False)
            phone_confirm_code = request.POST.get('phone_confirm_code', False)

            if phone:
                if not client.phone:
                    random_confirm_code = random.randint(10000,99999)

                    # TODO: check phone format
                    Clients.objects.filter(user=client.user).update(phone=phone)
                    Clients.objects.filter(user=client.user).update(phone_confirm_code=random_confirm_code)
                    added_phone = phone

                    args = {}
                    args['api_id'] = "0881834C-E81D-4F95-DCF2-D000B667FEEA"
                    args['to'] = phone
                    args['text'] = "PTPGO код подтверждения телефона: %s" % random_confirm_code
                    url = "http://sms.ru/sms/send?%s" % (urllib.parse.urlencode(args))
                    resp = urllib.request.urlopen(url).read().decode()

            elif phone_confirm_code:
                if not client.phone_confirmed:
                    if phone_confirm_code == client.phone_confirm_code:
                        Clients.objects.filter(user=client.user).update(phone_confirmed=True)
                        Clients.objects.filter(user=client.user).update(phone_confirm_code='')
                        phone_confirmed = True


    template = loader.get_template('pages/client/add_phone.html')
    template_args = {
        'request': request,
        'title': 'Добавить телефонный номер',
        'header_class': 'undefined',
        'added_phone': added_phone,
        'phone_confirmed': phone_confirmed,
    }
    return StreamingHttpResponse(template.render(template_args, request))


def signout(request):

    referer = utility.get_referer(request)

    if not request.user.is_authenticated():
        return HttpResponseRedirect(referer)


    logout(request)
    return HttpResponseRedirect(referer)


def cabinet(request):

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    template = loader.get_template('pages/client/cabinet.html')
    template_args = {
        'request': request,
        'title': 'Кабинет',
        'header_class': 'undefined',
    }
    return StreamingHttpResponse(template.render(template_args, request))


def pass_reset(request):
    pass