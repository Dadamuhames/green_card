from django.core.paginator import Paginator
from datetime import datetime
# pagination
def paginate(queryset, request, number):
    paginator = Paginator(queryset, number)

    try:
        page_obj = paginator.get_page(request.GET.get("page"))
    except:
        page_obj = paginator.get_page(request.GET.get(1))

    return page_obj


# get lst data
def get_lst_data(queryset, request, number):
    lst_one = paginate(queryset, request, number)
    page = request.GET.get('page')

    if page is None or int(page) == 1:
        lst_two = range(1, number + 1)
    else:
        start = (int(page) - 1) * number + 1
        end = int(page) * number

        if end > len(queryset):
            end = len(queryset)

        lst_two = range(start, end + 1)

    return dict(pairs=zip(lst_one, lst_two))



# filter by date
def filter_by_date(queryset, request):
    clients = queryset.order_by("agent_date")
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

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