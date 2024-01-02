from django.contrib.auth.models import User 
from django.db import models
from django.core.files import File

from io import BytesIO
from PIL import Image 

# -- Create your models here.
class Category(models.Model):
    title = models.CharField(max_length = 50) 
    slug = models.SlugField(max_length = 50)  # url representation field

    # give to Category plural form of Categories
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.title
    

# -- Create model Products
class Product(models.Model):
    DRAFT = 'draft'
    WAITING_APPROVAL = 'waitingapproval'
    ACTIVE = 'active'
    DELETED = 'deleted'

    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (WAITING_APPROVAL, 'Waiting Approval'),
        (ACTIVE, 'Active'),
        (DELETED,'Deleted'),
    )


    # connect product with paticular category
    user = models.ForeignKey(User, related_name = 'products',on_delete = models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/product_images/', blank=True, null=True)
    thumbnails = models.ImageField(upload_to='uploads/product_images/thumbnail/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        ordering=('-created_at',) # put items in oder they was created
        #from new to old (FIFO)

    def __str__(self):
        return self.title
    
    def get_display_price(self):
        return self.price/100
    
    def get_thumbnail(self):
        if self.thumbnails:
            return self.thumbnails.url
        else:
            if self.image:
                self.thumbnails = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnails.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'


    
# --- function making portfolio  --- 
    def make_thumbnail(self, image, size = (300,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality = 85)
        name = image.name.replace('uploads/product_images/','')
        thubnail = File(thumb_io,name = name)

        return thubnail
