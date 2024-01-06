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
    

# ------ Create model Products-------
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
        thumbnail = File(thumb_io,name = name)

        return thumbnail

#create model for orders
#on_delete=models.SET_NULL we don't want delete orders if User was deleted
#want to know when order was created auto_now_add=True
class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null = True)
    is_paid = models.BooleanField(default =False)
    payment_intent = models.CharField(max_length = 255, null=True)
    created_by = models.ForeignKey(User,related_name='order',
                                   on_delete=models.SET_NULL,
                                   null=True)
    created_at = models.DateTimeField(auto_now_add=True)

# model for orders list
class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items',on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)


    def get_total_price(self):
        return self.price/100

