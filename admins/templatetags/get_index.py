from django.template.defaulttags import register


@register.filter
def index(queryset, item):
    lst = [it.id for it in queryset]   


    if item.id not in lst:
        return None

    return lst.index(item.id) + 1
