from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # this one to one field is used so that we can add other things to user as well and it does not show error

    # additional
    portfolio_site=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)


    def __str__(self):
        return self.user.username
