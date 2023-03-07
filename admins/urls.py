from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("save_images", views.save_images, name='save_images'),
    path('filials', views.FilialList.as_view(), name='filials'),
    path("operators", views.OperatorsList.as_view(), name='operators'),
    path('agents', views.AgentsList.as_view(), name='agents'),
    path("clients", views.ClientsList.as_view(), name='clients'),
    path("clients/create", views.ClientsCreate.as_view(), name='clients_create'),
    path('clients/<int:pk>', views.ClientsDetailView.as_view(), name='clients_detail'),
    path('clients/<int:pk>/edit', views.ClientEdit.as_view(), name='clients_edit'),
    path('filials/create', views.create_filial, name='filials_create'),
    path("operators/create", views.create_operator, name='operators_create'),
    path("agents/create", views.create_agent, name='agents_create'),
    path("get_user", views.get_user, name='get_user'),
    path('login', LoginView.as_view(
        template_name='admins/sing-in.html',
        success_url='/admin/',
    ), name='login_admin'),
    path("delete_user_info", views.delete_user, name='del_user'),
    path('logout', views.logout_view, name='logout_url'),
    path('add_comment', views.add_comment, name='add_comment'),
    path("delete_client/<int:pk>", views.delete_client, name='del_client'),
    path("change_status", views.change_status, name='change_client_status'),
    path("images/delete", views.delete_image, name='del-img'),
    path("client_file/delete", views.dleete_client_file, name='del_client_file'),
    path("check_username", views.check_username, name='check_username')
]
