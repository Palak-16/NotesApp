from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User (when a user will be deleted all his notes will be deleted too)
    title = models.CharField(max_length=255) 
    content = models.TextField()  
    created_at = models.DateTimeField(auto_now_add=True) 

def __str__(self):
        return self.title  # Show title in admin panel    