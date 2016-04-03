from django.http import StreamingHttpResponse
from django.template import loader


def robots(request):
    template = loader.get_template('service/robots.txt')
    template_args = {
        'request': request,
    }
    return StreamingHttpResponse(template.render(template_args, request), content_type='text/plain')