from django.forms import ModelForm
from .models import Clients, ClientComments

class ClientForm(ModelForm):
    class Meta:
        model = Clients
        exclude = ['status']



class CommentForm(ModelForm):
    class Meta:
        model = ClientComments
        exclude = ['date']