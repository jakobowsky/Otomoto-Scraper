from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
from .models import *
from . import carScraperV1



def home(request):
    #x = carScraperV1.getDetails('https://www.otomoto.pl/oferta/audi-a6-zadbany-bezwypadkowy-zarejestrowany-ID6BxPWD.html#49db8497f3','1')

    #context = carScraperV1.findCars('Toyota',1)
    context = {}
    #updateData('audi')

    #updateData('bmw')

    return render(request,'carsViewer/homepage.html',context)

def report(request,carBrandName):
    if request.method == "POST":
        updateData(carBrandName)
    cars = []
    carsObj = Car.objects.filter(car_brand=str(carBrandName))
    for carObj in carsObj:
        car = {
            'model': carObj.car_model,
            'link': carObj.car_link,
            'brand':carObj.car_brand,
            'photo':carObj.car_photo,
            'year':carObj.car_year,
            'type':carObj.car_type,
            'engine':carObj.car_engine
        }
        cars.append(car)
    context = {'cars':cars,'brand':carBrandName}
    return render(request, 'carsViewer/report.html',context)

def updateData(carBrandName):

    CarBrand(car_brand=str(carBrandName)).save()
    newCarBrand = CarBrand(car_brand=str(carBrandName))
    cars = carScraperV1.findCars(carBrandName,1)
    for car in cars:
        new_car = Car(car_model=str(car['model']),
                      car_link=str(car['link']),
                      car_brand=newCarBrand,
                      car_photo=str(car['photo']),
                      car_year=str(car['year']),
                      car_type=str(car['type']),
                      car_engine=str(car['engine']))
        new_car.save()
    print('Database updated')





