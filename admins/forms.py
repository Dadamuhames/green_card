from django.forms import ModelForm
from .models import Clients, ClientComments

class ClientForm(ModelForm):
    class Meta:
        model = Clients
        exclude = ['agent', 'filial', 'operator', 'agent_date', 'operator_date', 'last_update', 'agent_name']


class CommentForm(ModelForm):
    class Meta:
        model = ClientComments
        exclude = ['date']