from django.http import StreamingHttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('pages/index.html')
    template_args = {
        'request': request,
        'title': 'Index page',
        'header_class': 'header--index',
    }
    return StreamingHttpResponse(template.render(template_args, request))


def boats(request):
    template = loader.get_template('pages/boats.html')
    template_args = {
        'request': request,
        'title': 'Boats list',
        'header_class': 'undefined',
    }
    return StreamingHttpResponse(template.render(template_args, request))


def robots(request):
    template = loader.get_template('service/robots.txt')
    template_args = {
        'request': request,
    }
    return StreamingHttpResponse(template.render(template_args, request), content_type='text/plain')