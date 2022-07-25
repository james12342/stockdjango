from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse
# Default User model
from django.contrib.auth.models import User

from embed_video.fields import EmbedVideoField

# Create your models here.

# Author Model
class Author(models.Model):
    #user = models.OneToOneField(User, on_delete = models.CASCADE)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(default="default-profile-pic.png", upload_to='uploads/profile-pictures', null=True)

    def __str__(self):
        return self.user.username

# Ads Model
class Ads(models.Model):
    
    CONDITION = (
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    )

    ADPOSTBY = (
        ('Superuser', 'Superuser'),
        ('Author', 'Author'),
        ('AutoAssigned', 'AutoAssigned'),
        
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    
    title = models.CharField(max_length=200)
    description = RichTextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    country=models.ForeignKey('country', on_delete=models.CASCADE, null=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE, null=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True) 
    condition = models.CharField(max_length=100, choices=CONDITION)
    brand = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    adPostBy= models.CharField(max_length=100, choices=ADPOSTBY)
    
    postJavascript=models.CharField(blank=True,max_length=5000)
    postImageUrl=models.CharField(blank=True,max_length=2000)
    postADUrl=models.CharField(blank=True,max_length=2000)
    postADClickCount=models.IntegerField(blank=True,null=True)
    postADClickPerEarn=models.DecimalField(max_digits=9, decimal_places=5,default=0)
    postADTotalEarn=models.DecimalField(max_digits=9, decimal_places=5,default=0)
    postADMaxEarn=models.DecimalField(max_digits=9, decimal_places=5,default=0)
    

    postIPaddress=models.ForeignKey('postIPaddress', on_delete=models.CASCADE, null=True)  
    postADViewerIP=models.ForeignKey('postADViewerIP', on_delete=models.CASCADE, null=True)

    postADReceivePaymentMethod=models.CharField(blank=True,max_length=50)
    postADPaymentReceiveAccount=models.CharField(blank=True,max_length=1000)
    postADPaymentTotalReceived=models.DecimalField(max_digits=9, decimal_places=5,default=0)
    postADPaymentReceiveable=models.DecimalField(max_digits=9, decimal_places=5,default=0)
    postADPaymentReceiveStatus=models.CharField(blank=True,max_length=50)
    postADPaymentLatestReceiveDate=models.DateTimeField(blank=True,null=True)

    video = EmbedVideoField(null=True, blank=True) 
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "Classified Ads"

    def __str__(self):
        return self.title


#Ad Viewer Activity Model
class AdViewerActivity(models.Model):    
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    AdID = models.IntegerField(blank=True,null=True)
    viewerIP=models.CharField(blank=True,max_length=50)
    viewerCountry=models.CharField(blank=True,max_length=50)
    viewerState=models.CharField(blank=True,max_length=50)
    viewerCity=models.CharField(blank=True,max_length=50)
    viewerZip=models.CharField(blank=True,max_length=50)
    viewerTimezone=models.CharField(blank=True,max_length=50)
    viewerIsp=models.CharField(blank=True,max_length=50)
    viewerLat=models.CharField(blank=True,max_length=50)
    viewerLon=models.CharField(blank=True,max_length=50)
    viewerViewTime=models.DateTimeField(blank=True,null=True)
    viewerViewDuration=models.DateTimeField(blank=True,null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    class Meta:
        verbose_name_plural = "Ad Viewer Activity"

    def __str__(self):
        return self.viewerIP+"_ADID_"+str(self.AdID)+"_Author_"+str(self.author)

# postIPaddress Model
class postIPaddress(models.Model):
    postIPaddress_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from postIPaddress name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.postIPaddress_name:
            self.slug = slugify(self.postIPaddress_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Poster IP address"

    def __str__(self):
        return self.postIPaddress_name



# postADViewerIP Model
class postADViewerIP(models.Model):
    postADViewerIP_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from postIPaddress name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.postADViewerIP_name:
            self.slug = slugify(self.postADViewerIP_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Poster AD Viewers IPs"

    def __str__(self):
        return self.postADViewerIP_name


# Country Model
class country(models.Model):
    country_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from state name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.country_name:
            self.slug = slugify(self.country_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "country"

    def __str__(self):
        return self.country_name


# State Model
class State(models.Model):
    state_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from state name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.state_name:
            self.slug = slugify(self.state_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return self.state_name

# City Model
class City(models.Model):
    city_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from city name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.city_name:
            self.slug = slugify(self.city_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city_name

# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_image = models.ImageField(upload_to='uploads/category', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    # overriding save method to add slug field from category name if not provided
    def save(self, *args, **kwargs):
        if not self.slug and self.category_name:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

# Image Model
class AdsImages(models.Model):
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d', default=None)

    def __str__(self):
        return self.ads.title

    class Meta:
        verbose_name_plural = 'Classified Ads Images'

# Top Banner Model
class AdsTopBanner(models.Model):
    title = models.CharField(max_length=200, default="Place Your Ad", blank=True)
    image = models.ImageField(upload_to='banners/%Y/%m/%d', default=None)

    def __str__(self):
        return self.title

# Right Banner Model
class AdsRightBanner(models.Model):
    title = models.CharField(max_length=200, default="Place Your Ad", blank=True)
    image = models.ImageField(upload_to='banners/%Y/%m/%d', default=None)

    def __str__(self):
        return self.title

# Bottom Banner Model
class AdsBottomBanner(models.Model):
    title = models.CharField(max_length=200, default="Place Your Ad", blank=True)
    image = models.ImageField(upload_to='banners/%Y/%m/%d', default=None)

    def __str__(self):
        return self.title

    



    
    

