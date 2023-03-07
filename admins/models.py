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
    STATUS = [('new', 'Yangi mijoz'),
              ('recieved', 'Operator qabul qildi'), ('contacted', 'Mijozga aloqaga chiqildi'),
              ('paid', 'To‘lov qilindi'), ('cancelled', 'Operator tomonidan bekor qilish'),
              ("accepted", "GreenCard oldi"), ("rejected", "GreenCard tomonidan bekor qilindi")]
    EDUCATIONS = [("Oliy", 'Oliy'), ('Orta', 'Orta')]
    FAMILY = [('Boydoq', 'Boydoq'), ('Uylangan', 'Uylangan'), ("Turmishga chiqgan", "Turmishga chiqgan")]

    full_name = models.CharField("Full name", max_length=255, blank=True, null=True)
    bith_date = models.DateField('Birth date', blank=True, null=True, default=None)
    adres = models.CharField("Adres", blank=True, null=True, max_length=255)
    nbm = models.CharField('Nbm', max_length=255, blank=True, null=True)
    sex = models.CharField("Sex", max_length=255, choices=GANDERS, blank=True, null=True)
    education = models.CharField("Education", max_length=255, blank=True, null=True, choices=EDUCATIONS)
    family_status = models.CharField('Family status', blank=True, null=True, choices=FAMILY, max_length=255)
    child_count = models.PositiveIntegerField('Child count', blank=True, null=True, default=0)
    spouse = models.CharField("Spouse", blank=True, null=True, max_length=255)
    spouse_birth_date = models.DateField(blank=True, null=True, default=None)
    spouse_education = models.CharField(max_length=255, blank=True, null=True)
    operator = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='operator_clients')
    oper_date = models.DateTimeField(blank=True, null=True)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='agent_users')
    agent_name = models.CharField("Agent name", max_length=255, blank=True, null=True)
    agent_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        "Status", max_length=255, default='new', choices=STATUS, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    filial = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='clients', blank=True, null=True)


    def get_agent(self):
        if self.agent:
            return str(self.agent.first_name) + ' ' + str(self.agent.last_name)
        

    def get_percent(self):
        fields = self._meta.fields
        count = len(fields)
        not_null = 0

        data_dict = self.__dict__
        for field in fields:
            key = str(field.name)
            if str(field.get_internal_type()) == 'ForeignKey':
                key += '_id'
            if data_dict[key] != None:
                not_null += 1
        
        perc = not_null * 100 // count


        return perc


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


