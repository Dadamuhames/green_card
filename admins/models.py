from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField
# Create your models here.


# types
class UserInfo(models.Model):
    STATUS = [('Active', 'Active'), ('Inactive', 'Inactive')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info', unique=True)
    name = models.CharField('Name', max_length=255, blank=True, null=True)
    is_filial = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_operator = models.BooleanField(default=False)
    nbm = models.CharField("nbm", max_length=255)
    status = models.CharField("Status", default='Active', max_length=255, choices=STATUS, blank=True, null=True)
    filial = models.ForeignKey("self", on_delete=models.CASCADE, related_name='workers', blank=True, null=True)


    def get_operators(self):
        return self.workers.filter(is_operator=True)
    
    def get_agents(self):
        return self.workers.filter(is_agent=True)



# clients
class Clients(models.Model):
    GANDERS = [("Erkak", "Erkak"), ('Ayol', 'Ayol')]
    STATUS = [('Yangi mijoz', 'Yangi mijoz'),
              ('Operator qabul qildi', 'Operator qabul qildi'), ('Mijozga aloqaga chiqildi', 'Mijozga aloqaga chiqildi'), 
              ('To‘lov qilindi', 'To‘lov qilindi'), ('Operator tomonidan bekor qilish', 'Operator tomonidan bekor qilish'), 
              ("GreenCard oldi", "GreenCard oldi"), ("GreenCard tomonidan bekor qilindi", "GreenCard tomonidan bekor qilindi")]
    EDUCATIONS = [("Oliy", 'Oliy'), ('Orta', 'Orta')]
    FAMILY = [('Some', 'Some')]

    full_name = models.CharField("Full name", max_length=255, blank=True, null=True)
    bith_date = models.DateField('Birth date', blank=True, null=True)
    adres = models.CharField("Adres", blank=True, null=True, max_length=255)
    nbm = models.CharField('Nbm', max_length=255, blank=True, null=True)
    sex = models.CharField("Sex", max_length=255, choices=GANDERS, blank=True, null=True)
    education = models.CharField("Education", max_length=255, blank=True, null=True, choices=EDUCATIONS)
    family_status = models.CharField('Family status', blank=True, null=True, max_length=255)
    child_count = models.PositiveIntegerField('Child count', blank=True, null=True)
    spouse = models.CharField("Spouse", blank=True, null=True, max_length=255)
    spouse_birth_date = models.DateField(blank=True, null=True)
    spouse_education = models.CharField(max_length=255, blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='operator_clients')
    oper_date = models.DateTimeField(blank=True, null=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='agent_users')
    agent_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField("Status", max_length=255, default='Yangi mijoz', choices=STATUS, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    filial = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='clients', blank=True, null=True)


    def get_agent(self):
        if self.agent:
            return str(self.agent.first_name) + ' ' + str(self.agent.last_name)


# client images
class ClientImages(models.Model):
    image = ThumbnailerImageField(upload_to='client_images')
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='images')


# client files
class ClientFiles(models.Model):
    file = models.FileField(upload_to='client_fiels')
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='files')


# client comments
class ClientComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    date = models.DateTimeField("Date", auto_now_add=True)
    cliet = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()


