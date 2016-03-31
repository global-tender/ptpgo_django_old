from django.http import StreamingHttpResponse
from django.template import loader

def signin(request):

    template = loader.get_template('auth/signin.html')
    template_args = {
        'request': request,
    }
    return StreamingHttpResponse(template.render(template_args, request))


def robots(request):
    template = loader.get_template('service/robots.txt')
    template_args = {
        'request': request,
    }
    return StreamingHttpResponse(template.render(template_args, request), content_type='text/plain')