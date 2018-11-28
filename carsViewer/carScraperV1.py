import requests
from bs4 import BeautifulSoup
import random

def getProxies():
    proxiesUrl = 'https://free-proxy-list.net/'
    request = requests.get(proxiesUrl).text
    soup = BeautifulSoup(request,'html.parser')
    proxies = set()
    proxiesTable = soup.find(id='proxylisttable')
    # save proxies in list
    for proxyRow in proxiesTable.tbody.find_all('tr'):
        proxies.add(str(proxyRow.find_all('td')[0].string) + ':' + str(proxyRow.find_all('td')[1].string))
    return proxies

def getWorkingProxy():
    proxies = getProxies()
    for proxy in proxies:
        try:
            response = requests.get('https://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=3)
            return proxy
        except: pass

def getLinksToCars(carBrand,pages): #working on used cars
    proxy = getWorkingProxy()
    counter = 1
    cars = set()
    while(counter <= pages):
        link = 'https://www.otomoto.pl/osobowe/uzywane/{}/?page={}'.format(carBrand, counter)
        try:
            r = requests.get(link,proxies={"http": proxy, "https": proxy},timeout=3)
            soup = BeautifulSoup(r.text,'html.parser')
            items = soup.find_all(class_='adListingItem')
            for item in items:
                cars.add(item.find('a',class_='offer-title__link').get('href'))
                #linkOfCar = item.find('a',class_='offer-title__link').get('href')
            counter+=1
        except:
            print('getting new proxy')
            proxy = getWorkingProxy()
    return cars

def getDetails(linkToCar,proxy):
    infoAboutCar = {}
    try:
        #r = requests.get(linkToCar)
        r = requests.get(linkToCar, proxies={"http": proxy, "https": proxy}, timeout=3)
        soup = BeautifulSoup(r.text, 'html.parser')
        top = soup.find('div',class_="offer-content__gallery")
        #print(top.find('div',class_='photo-item').img.get('data-src'))
        #photo = soup.find('div', class_='photo-item')
        #photo = (photo.img.get('src'))
        photo = (top.find('div',class_='photo-item').img.get('src'))
        if photo == None:
            photo = (top.find('div',class_='photo-item').img.get('data-src'))
        #print(photo)
        infoAboutCar['photo'] = photo
        tab = soup.find(class_='offer-params')
        columns = tab.find_all(class_='offer-params__list')
        for item in columns:
            rows = item.find_all(class_='offer-params__item')
            for row in rows:
                x = row.find(class_='offer-params__label').string
                y = row.find(class_='offer-params__value').get_text().replace('\n','').strip()
                infoAboutCar[x] = y

    except:
        print('getting new proxy')
        proxy = getWorkingProxy()

    return infoAboutCar

def findCars(carBrand,pages):
    links = getLinksToCars(carBrand,pages)
    proxy = getWorkingProxy()
    newCars = []
    i = 0 # how many cars will be added
    for link in links:
        if i == 15:
            break
        try:
            infoAboutCar = getDetails(link,proxy)
            #link,model,brand,year,type_car,engine
            actualCar = {
                "link" : str(link),
                "model" : infoAboutCar['Model pojazdu'],
                "brand" : infoAboutCar['Marka pojazdu'],
                "year" : infoAboutCar['Rok produkcji'],
                "type" : infoAboutCar['Typ'],
                "photo" : infoAboutCar['photo'],
                "engine" :infoAboutCar['Rodzaj paliwa']
            }
            newCars.append(actualCar)
            print('Car added: ',infoAboutCar['Marka pojazdu'],' ',infoAboutCar['Model pojazdu'])
            i+=1
        except:
            print('getting new proxy')
            proxy = getWorkingProxy()
    return newCars




