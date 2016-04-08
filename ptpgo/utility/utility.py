
def get_referer(request):

    referer = request.META.get('HTTP_REFERER', '/')

    host = (request.is_secure() and 'https://' or 'http://') + request.META['HTTP_HOST']

    if not referer.startswith(host):
        referer = '/'

    return referer