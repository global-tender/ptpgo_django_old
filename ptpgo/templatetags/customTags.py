from django import template
from ptpgo.models import ListBoat

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_user_boats(context):
    try:
        request = context['request']
        boats = ListBoat.objects.filter(user=request.user).first()
        if boats:
            return True
        else:
            return False
    except Exception as e:
        return False