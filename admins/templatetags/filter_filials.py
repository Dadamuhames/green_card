from django.template.defaulttags import register


@register.filter
def filter_filial(queryset, status):
    return queryset.filter(status=status)