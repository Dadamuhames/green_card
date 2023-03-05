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
# Create your views here.


# save images
def save_images(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        file = request.FILES.get('file')
        id = request.POST.get("id")

        request.session[f'clients_{key}'] = request.session.get('clients', [])
        file_name = default_storage.save('dropzone/' + file.name, file)

        data = {
            'id': id,
            'name': file_name
        }

        request.session[f'clients_{key}'].append(data)
        request.session.modified = True

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

        context['objects'] = get_lst_data(self.get_queryset(), self.request, paginate_by)
        context['page_obj'] = paginate(self.get_queryset(), self.request, paginate_by)
        context['filials'] = UserInfo.objects.filter(is_filial=True)
        context['page_size'] = paginate_by

        pang_url = self.request.path + '?'

        for key, val in self.request.GET.items():
            if key != 'page':
                pang_url += f'{key}={val}&'

        context['pgn_url'] = pang_url


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
        queryset = Clients.objects.all()
        user = self.request.user

        status = self.request.GET.get("status", '')
        q = self.request.GET.get("q", '')

        if not user.is_superuser:
            if user.info.is_operator:
                queryset = queryset.filter(filial=user.info.filial)
                if status == 'Operator qabul qildi':
                    queryset = queryset.filter(operator=user)
                    status = ''

            elif user.info.is_filial:
                queryset = queryset.filter(filial=user.info)

            elif user.info.is_agent:
                queryset = queryset.filter(agent=user)

        
        if q != '':
            queryset = queryset.filter(Q(full_name__iregex=q))

        if status != '':
            queryset = queryset.filter(status=status)

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

        return context




        '''if not user.is_superuser:
            if user.info.is_agent or user.info.is_operator:
                context['operators'] = UserInfo.objects.filter(filial=user.info.filial).filter(is_operator=True)
                context['agents'] = UserInfo.objects.filter(filial=user.info.filial).filter(is_agent=True)
            elif user.info.is_filial:
                context['operators'] = UserInfo.objects.filter(filial=user.info).filter(is_operator=True)
                context['agents'] = UserInfo.objects.filter(filial=user.info).filter(is_agent=True)'''


        return context

    

# clients create
class ClientsCreate(CreateView):
    model = Clients
    fields = '__all__'
    template_name = ''


    def get(self, request, *args, **kwargs):
        user = request.user

        if not user.is_superuser:
            if user.info.is_agent == False:
                return redirect("/admin/")


        return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        agent = self.request.user

        if agent.info.is_agent:
            client = form.save()

            client.agent = agent
            client.filial = agent.filial
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

            return client
        

    def post(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_superuser == False and user.info.is_agent == False:
            return redirect('/admin/')

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
                if inst.operator and inst.operator != user.info:
                    return redirect("/admin/")
                elif inst.operator is None:
                    inst.operator = user.info
                    inst.oper_date = datetime.now()
                    inst.save()
            elif user.info.is_agent:
                if inst.agent != user.info:
                    return redirect("")

        return super().get(request, *args, **kwargs)

    



# client edit
class ClientEdit(UpdateView):
    model = Clients
    fields = '__all__'
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
                if inst.operator and inst.operator != user.info:
                    return redirect("/admin/")
                elif inst.operator is None:
                    inst.operator = user.info
                    inst.oper_date = datetime.now()
                    inst.save()
            elif user.info.is_agent:
                if inst.agent != user.info:
                    return redirect("")

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
        
