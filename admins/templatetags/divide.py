from django.template.defaulttags import register


@register.filter
def div(nbm, n):
    return nbm // n
