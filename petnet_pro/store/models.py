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
    

#Create model Products
class Product(models.Model):
    # connect product with paticular category
    user = models.ForeignKey(User, related_name = 'products',on_delete = models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering=('-created_at',) # put items in oder they was created
        #from new to old (FIFO)

    def __str__(self):
        return self.title
    
    def get_display_price(self):
        return self.price/100
