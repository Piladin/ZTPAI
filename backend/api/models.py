from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class SystemUser(AbstractUser):

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set", 
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  
        blank=True,
    )
    
class Announcement(models.Model):
    subject = models.CharField(max_length=255)
    content = models.TextField()
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    author = models.ForeignKey(SystemUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title