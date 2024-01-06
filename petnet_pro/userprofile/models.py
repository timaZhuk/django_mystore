from django.contrib.auth.models import User  
from django.db import models

# Create your models here.

class Userprofile(models.Model):
    #OneToOne means we create only one user for prfofile
    user = models.OneToOneField(User,related_name = 'userprofile',
                                on_delete = models.CASCADE)
    is_vendor = models.BooleanField(default = False)
    

    #user realted to 'userprofile app'
    # on_delete = models.CASCADE is If we delete the user all data will be deleted too

#---string representation of User
    def ___str__(self):
        return self.user.username