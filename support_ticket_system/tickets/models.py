from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = [
    ('ENDUSER', 'End User'),
    ('ITMANAGER', 'IT Manager'),
    ('OTHERMANAGER', 'Other Manager'),
    ('ITSTAFF', 'IT Staff'),
]

    




class Kullanici(models.Model):
    full_name = models.CharField(max_length=255)
    login_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ENDUSER')
    def __str__(self):
        return self.full_name



class Yer(models.Model):
    goruntu_adi = models.CharField(max_length=100)
    kisa_ad = models.CharField(max_length=50)
    tanim = models.TextField(blank=True, null=True)
    genel_yap = models.BooleanField(default=False)
    kullanicilar = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='yer_kullanicilari')  
    
    def save(self, *args, **kwargs):
        self.goruntu_adi = slugify(self.goruntu_adi)
        super(Yer, self).save(*args, **kwargs)

    def __str__(self):
        return self.goruntu_adi


class CustomUser(AbstractUser):
    language = models.CharField(max_length=10, choices=[('EN', 'English'), ('TR', 'Turkish')], default='EN')
    yerler = models.ManyToManyField(Yer, blank=True, related_name='custom_user_yerler')  
    is_active = models.BooleanField(default=True)
    
    
class ProgramModule(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ticket(models.Model):

    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("open", "Open"), ("closed", "Closed")], default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.CharField(max_length=200)
    details = models.TextField()
    company = models.ForeignKey(Yer, on_delete=models.CASCADE)
    program_module = models.ForeignKey(ProgramModule, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(max_length=50, choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ])
    severity = models.CharField(max_length=50, choices=[
        ('Minor', 'Minor'),
        ('Major', 'Major'),
        ('Critical', 'Critical')
    ])
    special_group = models.CharField(max_length=50, blank=True, null=True)
    ticket_type = models.CharField(max_length=50, blank=True, null=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tickets_assigned'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tickets_created'
    )
    email_notification = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='email_notifications'
    )
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.summary


class TicketUpdate(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE, related_name="updates")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(max_length=20, choices=[("open", "Open"), ("closed", "Closed")])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ticket.id} - {self.user.username} - {self.status}"