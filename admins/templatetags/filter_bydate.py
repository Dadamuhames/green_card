from django.template.defaulttags import register
from datetime import datetime

@register.filter
def by_date(queryset, data : dict):
    request = data.get('request')
    type = data.get("type")


    clients = queryset.order_by("agent_date")

    if type == 'agent':
        from_date = request.GET.get('agent_from_date')
        to_date = request.GET.get('agent_to_date')
    elif type == 'operator':
        from_date = request.GET.get('operator_from_date')
        to_date = request.GET.get('operator_to_date')
    elif type == 'filial':
        from_date = request.GET.get('filial_from_date')
        to_date = request.GET.get('filial_to_date')

    if clients.exists():
        if from_date:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
        else:
            from_date = clients.first().agent_date

        if to_date:
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
        else:
            to_date = datetime.today()

        if from_date and to_date:
            queryset = queryset.filter(
                agent_date__gte=from_date, agent_date__lte=to_date)

    return queryset
