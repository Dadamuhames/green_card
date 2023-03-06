from django.shortcuts import render, redirect
from django.views.generic import ListView, UpdateView, CreateView, DetailView
from django.contrib.auth.models import User
from .models import UserInfo, Clients, ClientFiles, ClientImages
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import logout
from django.core.files.storage import default_storage
from django.http import JsonResponse, QueryDict, HttpResponseRedirect
from .utils import *
from django.core.cache import cache
from .serializers import UserInfoSerializer
from .forms import ClientForm, CommentForm
from datetime import datetime
# Create your views here.


# delete image
def delete_image(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        file = request.POST.get("file")

        if request.session.get(key):
            for it in request.session[key]:
                if it['name'] == file:
                    request.session[key].remove(it)
                    request.session.modified = True

    return redirect(request.META.get("HTTP_REFERER"))


# save images
def save_images(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        file = request.FILES.get('file')
        id = request.POST.get("id")

        request.session[f'clients_{key}'] = request.session.get(
            f'clients_{key}', [])
        file_name = default_storage.save('dropzone/' + file.name, file)

        data = {
            'id': id,
            'name': file_name
        }

        request.session[f'clients_{key}'].append(data)
        request.session.modified = True

        print(request.session[f'clients_{key}'])

    return JsonResponse(file_name, safe=False)


# based list view
class BasedListView(ListView):
    cache_key = None

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser == False and (user.info.is_agent or user.info.is_operator):
            return redirect('/admin/')

        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        queryset = self.queryset.order_by("-id")
        user = self.request.user
    
        if user.is_superuser:
            filial_id = self.request.GET.get("filial", '')

            if filial_id != '':
                try:
                    filial = UserInfo.objects.filter(is_filial=True).get(id=filial_id)
                    queryset = queryset.filter(is_filial=False).filter(filial=filial)
                except:
                    pass
        elif user.info.is_filial:
            queryset = queryset.filter(filial=user.info)


        query = self.request.GET.get("q", '')

        if query != '':
            queryset = queryset.filter(Q(name__iregex=query) | Q(user__username__iregex=query) | Q(user__first_name__iregex=query) | Q(user__last_name__iregex=query))

        return queryset


    def get_paginate_by_castom(self):
        user_id = self.request.user.id
        paginate_by = cache.get_or_set(user_id, {}).get(self.cache_key)

        if paginate_by is None:
            paginate_by = 20
        else:
            paginate_by = int(paginate_by)

        page_size = self.request.GET.get("page_size", '')

        if page_size != '':
            try:
                paginate_by = int(page_size)
                user_cache = cache.get_or_set(user_id, {})
                user_cache[self.cache_key] = paginate_by
                cache.set(user_id, user_cache)
            except:
                pass

        return paginate_by
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginate_by = self.get_paginate_by_castom()
        print(paginate_by)
        page_obj = paginate(self.get_queryset(), self.request, paginate_by)

        context['objects'] = get_lst_data(self.get_queryset(), self.request, paginate_by)
        context['page_obj'] = page_obj
        context['filials'] = UserInfo.objects.filter(is_filial=True)
        context['page_size'] = paginate_by

        pang_url = self.request.path + '?'

        for key, val in self.request.GET.items():
            if key != 'page':
                pang_url += f'{key}={val}&'

        context['pgn_url'] = pang_url
        print(pang_url)

        page_count = page_obj.paginator.num_pages
        print(page_count)
        curent_page = page_obj.number
        page_range = range(1, page_count+1)

        if page_count > 6:
            if curent_page+6 <= page_count:
                page_range = range(curent_page, curent_page+6)
            else:
                page_range = range(curent_page, page_count)

        #context['page_range'] = page_range = page_obj.paginator.get_elided_page_range(number=curent_page)
        #print(context['page_range'])
        #print(page_range)


        return context

    
# fillials view
class FilialList(BasedListView):
    queryset = UserInfo.objects.filter(is_filial=True)
    template_name = 'admins/user-filials.html'
    cache_key = 'filials_list'

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admins:clients')

        return super().get(request, *args, **kwargs)




# operators list
class OperatorsList(BasedListView):
    queryset = UserInfo.objects.filter(is_operator=True)
    template_name = 'admins/user-operator.html'
    cache_key = 'operators_list'


# agents list
class AgentsList(BasedListView):
    queryset = UserInfo.objects.filter(is_agent=True)
    template_name = 'admins/user-agent.html'
    cache_key = 'agents_list'


# clients list
class ClientsList(ListView):
    model = Clients
    template_name = 'admins/index.html'
    cache_key = 'clients_list'


    def get_paginate_by_castom(self):
        user_id = self.request.user.id
        paginate_by = cache.get_or_set(user_id, {}).get(self.cache_key)

        if paginate_by is None:
            paginate_by = 20
        else:
            paginate_by = int(paginate_by)

        page_size = self.request.GET.get("page_size", '')

        if page_size != '':
            try:
                paginate_by = int(page_size)
                user_cache = cache.get_or_set(user_id, {})
                user_cache[self.cache_key] = paginate_by
                cache.set(user_id, user_cache)
            except:
                pass

        return paginate_by

    def get_queryset(self):
        queryset = Clients.objects.order_by("-id")
        user = self.request.user

        status = self.request.GET.get("status", '')
        q = self.request.GET.get("q", '')
        operator_id = self.request.GET.get("operator")
        agent_id = self.request.GET.get("agent")
        filial_id = self.request.GET.get('filial')

        if not user.is_superuser:
            if user.info.is_operator:
                queryset = queryset.filter(filial=user.info.filial)
                if status == 'Yangi mijoz':
                    queryset = queryset.filter(operator__isnull=True)
                    status = ''
                else:
                    queryset = queryset.filter(operator=user)

            elif user.info.is_filial:
                queryset = queryset.filter(filial=user.info)

            elif user.info.is_agent:
                queryset = queryset.filter(agent=user)
        
        if user.is_superuser or user.info.is_filial:
            if operator_id:
                try:
                    operators = UserInfo.objects.filter(is_operator=True)
                    if user.info.is_filial:
                        operators.filter(filial=user.info)
                    
                    operator = operators.get(id=int(operator_id))
                    queryset = queryset.filter(operator=operator.user)
                except:
                    pass

            if agent_id:
                try:
                    agent = UserInfo.objects.filter(is_agent=True).get(id=int(agent_id))
                    queryset = queryset.filter(agent=agent.user)
                except:
                    pass
        
        if user.is_superuser:
            if filial_id:
                try:
                    filial = UserInfo.objects.filter(is_operator=True).get(id=int(filial_id))
                    queryset = queryset.filter(filial=filial)
                except:
                    pass


        
        if q != '':
            queryset = queryset.filter(Q(full_name__iregex=q))

        if status != '':
            queryset = queryset.filter(status=status)


        clients = queryset.order_by("agent_date")

        if clients.exists():
            from_date = self.request.GET.get('from_date')
            to_date = self.request.GET.get('to_date')

            if from_date:
                from_date = datetime.strptime(from_date, '%Y-%m-%d')
            else:
                from_date = clients.first().agent_date


            if to_date:
                to_date = datetime.strptime(to_date, '%Y-%m-%d')
            else:
                to_date = datetime.today()

            if from_date and to_date:
                queryset = queryset.filter(agent_date__gte=from_date, agent_date__lte=to_date)


        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginate_by = self.get_paginate_by_castom()

        context['objects'] = get_lst_data(
            self.get_queryset(), self.request, paginate_by)
        context['page_obj'] = paginate(
            self.get_queryset(), self.request, paginate_by)
        context['filials'] = UserInfo.objects.filter(is_filial=True)
        context['page_size'] = paginate_by

        user = self.request.user

        status_url = self.request.path + '?'

        for key, val in self.request.GET.items():
            if key != 'status':
                status_url += f'{key}={val}&'

        context['status_url'] = status_url


        pang_url = self.request.path + '?'

        for key, val in self.request.GET.items():
            if key != 'page':
                pang_url += f'{key}={val}&'

        context['pgn_url'] = pang_url

        if not user.is_superuser:
            if user.info.is_agent or user.info.is_operator:
                context['operators'] = UserInfo.objects.filter(filial=user.info.filial).filter(is_operator=True)
                context['agents'] = UserInfo.objects.filter(filial=user.info.filial).filter(is_agent=True)
            elif user.info.is_filial:
                context['operators'] = UserInfo.objects.filter(filial=user.info).filter(is_operator=True)
                context['agents'] = UserInfo.objects.filter(filial=user.info).filter(is_agent=True)

        return context

    

# clients create
class ClientsCreate(CreateView):
    model = Clients
    fields = '__all__'
    template_name = 'admins/client-create.html'


    def get(self, request, *args, **kwargs):
        user = request.user
        keys = ['clients_images', 'clients_files']

        for key in keys:
            if request.session.get(key):
                for it in list(request.session[key]):
                    if it['id'] == 'undefined':
                        request.session[key].remove(it)
                        request.session.modified = True

        if user.is_superuser or user.info.is_agent == False:
            return redirect("admins:clients")

        print(request.session.get('clients_images'))

        return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        agent = self.request.user

        if agent.is_superuser:
            return redirect("admins:clients")
        
        if agent.info.is_agent:
            client = form.save()

            client.agent = agent
            client.filial = agent.info.filial
            client.agent_date = datetime.now()
            client.last_update = datetime.now()
            client.save()

            files = self.request.session.get('clients_files')
            if files:
                files = [it for it in files if it['id'] == '']
                for file in files:
                    client_file = ClientFiles(client=client, file=file['name'])
                    client_file.save()

            images = self.request.session.get('clients_images')
            if images:
                images = [it for it in files if it['id'] == '']
                for file in images:
                    client_image = ClientImages(client=client, file=file['name'])
                    client_image.save()

            return redirect("admins:clients")
        

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_superuser or user.info.is_agent == False:
            return redirect('admins:clients')

        return super().post(request, *args, **kwargs)
    

# create clients
def client_create(request):
    agent = request.user

    if agent.is_superuser:
        return redirect("admins:clients")

    if agent.info.is_agent:
        form = ClientForm(request.POST)

        if form.is_valid():
            client = form.save()
            print(client.nbm)

            client.agent = agent
            client.filial = agent.info.filial
            client.agent_date = datetime.now()
            client.last_update = datetime.now()
            client.save()

            files = request.session.get('clients_files')
            if files:
                files = [it for it in files if it['id'] == '']
                for file in files:
                    client_file = ClientFiles(client=client, file=file['name'])
                    client_file.save()

            images = request.session.get('clients_images')
            if images:
                images = [it for it in files if it['id'] == '']
                for file in images:
                    client_image = ClientImages(
                        client=client, file=file['name'])
                    client_image.save()
        else:
            print(form.errors)

    
    return redirect('admins:clients')

    
# clients detail view
class ClientsDetailView(DetailView):
    model = Clients
    template_name = 'admins/inner.html'


    def get_queryset(self):
        queryset = Clients.objects.all()
        user = self.request.user

        if not user.is_superuser:
            if user.info.is_filial:
                queryset = queryset.filter(filial=user.info)
            elif user.info.is_agent or user.info.is_operator:
                queryset = queryset.filter(filial=user.info.filial)

        return queryset


    def get(self, request, *args, **kwargs):
        user = self.request.user
        inst = self.get_object()

        if not user.is_superuser:
            if user.info.is_operator:
                if inst.operator and inst.operator != user:
                    return redirect("admins:clients")
                elif inst.operator is None:
                    inst.operator = user
                    inst.oper_date = datetime.now()
                    inst.save()
            elif user.info.is_agent:
                if inst.agent != user:
                    return redirect("admins:clients")

        return super().get(request, *args, **kwargs)

    



# client edit
class ClientEdit(UpdateView):
    model = Clients
    form_class = ClientForm
    template_name = 'admins/inner-edit.html'

    def get_queryset(self):
        queryset = Clients.objects.all()
        user = self.request.user

        if not user.is_superuser:
            if user.info.is_filial:
                queryset = queryset.filter(filial=user.info)
            elif user.info.is_agent or user.info.is_operator:
                queryset = queryset.filter(filial=user.info.filial)

        return queryset

    def get(self, request, *args, **kwargs):
        user = self.request.user
        inst = self.get_object()

        if not user.is_superuser:
            if user.info.is_operator:
                if inst.operator and inst.operator != user:
                    return redirect("admins:clients")
                elif inst.operator is None:
                    inst.operator = user
                    inst.oper_date = datetime.now()
                    inst.save()
            elif user.info.is_agent:
                if inst.agent != user:
                    return redirect("admins:clients")

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        client = form.save()

        files = self.request.session.get('clients_files')
        if files:
            files = [it for it in files if str(it['id']) == str(client.id)]
            for file in files:
                client_file = ClientFiles(client=client, file=file['name'])
                client_file.save()

        images = self.request.session.get('clients_images')
        if images:
            images = [it for it in files if str(it['id']) == str(client.id)]
            for file in images:
                client_image = ClientImages(client=client, file=file['name'])
                client_image.save()

        client.last_update = datetime.now()
        client.save()

        return redirect("admins:clients")

    

    def post(self, request, *args, **kwargs):
        user = self.request.user
        inst = self.get_object()
        filial = None

        if not user.is_superuser:
            if user.info.is_filial:
                filial = user.info
            elif user.info.is_operator or user.info.is_agent:
                filial = user.info.filial


        if not user.is_superuser and inst.filial != filial:
            return redirect("/admin/")


        return super().post(request, *args, **kwargs)

        

def worker_create_perms(user):
    if not user.is_superuser:
        if user.info.is_operator or user.info.is_agent:
            return redirect("/admin/")


# def save user
def save_user(is_operator=False, is_agent=False, is_filial=False, request=None):
    worker_create_perms(request.user)
    username = request.POST.get("username")
    password = request.POST.get("password")
    status = request.POST.get('status')
    id = request.POST.get('id')

    is_active = status == 'Active'
    try:
        new_user = User.objects.get(id=int(id))
        if new_user.username != username:
            new_user.username = username
    except:
        new_user = User.objects.create(username=username)

    if password:
        print(new_user.password)
        new_user.set_password(password)
        print(new_user.password)
    new_user.is_active = is_active

    full_name = request.POST.get("full_name", '')

    if ' ' in full_name:
        first_name = full_name.split(' ')[0]
        last_name = full_name.split(' ')[-1]
        new_user.first_name = first_name
        new_user.last_name = last_name
    else:
        new_user.first_name = full_name

    new_user.save()

    nbm = request.POST.get("nbm", '')
    filial = request.POST.get("filial")
    name = request.POST.get('name')
    
    user = request.user

    if not user.is_superuser and user.info.is_filial:
        filial = user.info
    else:
        try:
            filial = UserInfo.objects.get(id=int(filial))
        except:
            filial = None
    
    new_user_info, created = UserInfo.objects.update_or_create(user=new_user)
    new_user_info.is_operator = is_operator
    new_user_info.is_agent = is_agent
    new_user_info.is_filial = is_filial
    new_user_info.nbm = nbm
    new_user_info.status = status
    new_user_info.name = name
    

    if filial and not is_filial:
        new_user_info.filial = filial

    new_user_info.save()

    return new_user


# create filial
def create_filial(request):
    if request.method == 'POST':
        user = save_user(is_filial=True, request=request)
        url = request.POST.get("url")

        print(user)

        return redirect(url)


# create operator
def create_operator(request):
    if request.method == 'POST':
        user = save_user(is_operator=True, request=request)
        url = request.POST.get("url")
        return redirect(url)

# create agent
def create_agent(request):
    if request.method == 'POST':
        user = save_user(is_agent=True, request=request)
        url = request.POST.get("url")
        return redirect(url)

# get user
def get_user(request):
    id = request.GET.get("id")

    try:
        user = UserInfo.objects.get(id=int(id))
        serializer = UserInfoSerializer(user)

        return JsonResponse(serializer.data)
    except:
        pass


    return JsonResponse("error", safe=False)


# delete user_info
def delete_user(request):
    id = request.POST.get("id")
    url = request.POST.get("url")

    try:
        User.objects.get(id=int(id)).delete()
    except:
        pass

    return redirect(url)


# logout
def logout_view(request):
    logout(request)

    return redirect('admins:login_admin')



# add comment 
def add_comment(request):
    url = request.POST.get("url")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)

    return redirect(url)
        

# delete client 
def delete_client(request, pk):
    try:
        client = Clients.objects.get(id=int(pk))
        if request.user == client.agent or request.user.info == client.filial or request.user.is_superuser:
            client.delete()
    except:
        pass

    return redirect("admins:clients")



# change client status
def change_status(request):
    if request.method == 'POST':
        id = request.POST.get("id")
        url = request.POST.get("url")
        status = request.POST.get("status")
        user = request.user

        try:
            client = Clients.objects.get(id=int(id))
            if client.operator == user or client.agent == user or user.is_superuser:
                client.status = status
                client.save()
        except:
            pass

        return redirect(url)

    return redirect("admins:clients")