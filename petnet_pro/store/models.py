from django.contrib.auth.models import User 
from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50) 
    slug =models.SlugField(max_length=50)  #url representation field

    # give to Category plural form of Categories
    class Meta:
        verbose_name_plural='Categories'
    
    def __str__(self):
        return self.title