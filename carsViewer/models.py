from django.db import models

# Create your models here.

class CarBrand(models.Model):
    car_brand = models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.car_brand

class Car(models.Model):
    car_model = models.CharField(max_length=100,null=True,blank=True)
    car_link =  models.CharField(max_length=100,null=True,blank=True)
    car_brand = models.ForeignKey(CarBrand,on_delete=models.CASCADE)
    car_photo = models.CharField(max_length=300,null=True,blank=True)
    car_year = models.CharField(max_length=100,null=True,blank=True)
    car_type = models.CharField(max_length=100,null=True,blank=True)
    car_engine = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return str(self.id) + ' ' + str(self.car_brand) + ' ' + str(self.car_model)
