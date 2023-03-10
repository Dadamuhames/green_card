from django.template.defaulttags import register


@register.filter
def filter_filial(queryset, status):
    if queryset is None:
        return 0
    return queryset.filter(status=status).count()