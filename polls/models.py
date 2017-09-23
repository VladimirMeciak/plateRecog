import datetime

from django.db import models
from django.utils import timezone
from PIL import Image





class Visitor(models.Model):
    name = models.CharField(max_length = 200)
    spz = models.CharField(max_length = 10)
    reg_date = models.DateTimeField('date registrated',blank=True,null=True)
    last_visit_date = models.DateTimeField('date visited',blank=True,null=True)
    comment = models.CharField(max_length = 500,blank=True,null=True)
    profile_image = models.ImageField(upload_to='images/profile_pics/',default='images/profile_pics/avatar.png',blank=True,null=True)
    allowed_date_from= models.DateField('allowed_date_from',blank=True,null=True)
    allowed_date_to= models.DateField('allowed_date_to',blank=True,null=True)
    allowed_time_from=models.TimeField('allowed_time_from',blank=True,null=True)
    allowed_time_to=models.TimeField('allowed_time_to',blank=True,null=True)

    def __str__(self):
       return (self.name + " - " + self.spz)

class Plate(models.Model):
    visitor = models.ForeignKey(Visitor, null=True,on_delete=models.CASCADE)
    spz= models.CharField(max_length = 200)
    corrSpz = models.CharField(max_length = 200,blank=True)
    cap_date = models.DateTimeField('date captured')
    image = models.ImageField(upload_to='images/plates')
    corr  = models.ImageField(upload_to='images/corrected',blank=True)
    arr_dep= models.IntegerField(default=0) #arrIVAL =1 depPARTURE = 2 unknown=0
    similarity=models.DecimalField(max_digits=10, decimal_places=8,default=0,blank=True)
    #Simage_url = models.URLField(null=True, blank=True)


    def __str__(self):
       return self.spz
