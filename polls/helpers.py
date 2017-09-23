import re
import requests
from bs4 import BeautifulSoup
import urllib.request

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from .models import Plate, Visitor

import datetime
from django.utils import timezone

import cv2
import numpy as np
from .plateCv import *

def save_image_from_url(model, url):
    r = requests.get(url)

    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()

    model.image.save("image.jpg", File(img_temp), save=True)




def get_plates_from_site(site,num=10):


    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]


    #for url in urls:
    for i in range(1,num):
        output= open('file'+ str(i) +'.jpg', 'wb')
        print ("SOM RTUUTU")
        response = requests.get(site + '/'+urls[i])
        output.write(response.content)
        output.close()

def imscrap(site):
    import image_scraper

    image_scraper.scrape_images(site)
    print ("SOM RTUUTU")


def get_plates_from_spz_print(site):


    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    table_tags=soup.find_all('tbody')


    tr_tags=table_tags[0].findAll('tr')
    #for element in table_tags:
        #print ("tolkoo elementoc")

    #print (str(tr_tags))
    for tr in tr_tags:
        #print (str(tr_tags))
        td_tags=tr.findAll('td')
        #print (str(td_tags))
        #print ("*************")
        print ("Cas  " + str(td_tags[0].get_text()) + "    SPZ    " + str(td_tags[1].get_text()) + "     url img   " + str(td_tags[2].img['src']) )
        #print (td_tags[2].img['src'])
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]


    #for url in urls:
    #for i in range(1,num):
        #output= open('file'+ str(i) +'.jpg', 'wb')
        #print ("SOM RTUUTU")
        #response = requests.get(site + '/'+urls[i])
        #output.write(response.content)
        #output.close()



def get_plates_from_spz_to_DB(site,num):

    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    table_tags=soup.find_all('tbody')
    tr_tags=table_tags[0].findAll('tr')

    for i in range(0,num):
        td_tags=tr_tags[i].findAll('td')
        r = requests.get(site + '/'+str(td_tags[2].img['src']))

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()

        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()




        date_time= datetime.datetime.strptime(str(td_tags[0].get_text()),"%H:%M:%S %d.%m %Y")
        spz=str(td_tags[1].get_text())
        try:
            visitor = Visitor.objects.get(spz=spz)
        except Visitor.DoesNotExist:
            visitor = Visitor.objects.get(spz='BA000XX')

        p=Plate(visitor=visitor,spz=spz, cap_date=date_time,image=None)
        p.image.save(str(td_tags[2].img['src']), File(img_temp), save=True)
        #p.corr.save(str(td_tags[2].img['src']), correctPlate(), save=True)
        p.save()
def save_corrected_plates(plates_l):
    for plate in plates_l:
        fileURL = correctPlate(plate=plate)
        print("otvaram corrected    "  +fileURL)
        reopen = open(fileURL, 'rb')
        django_file = File(reopen)
        plate.corr.save("image.jpg",django_file,save=True)
        plate.save()

def do_opencv(plate):
    print (str(plate.image.url))

    image = cv2.imread('polls/' + (plate.image.url))
    image = cv2.resize(image, (0,0), fx=3, fy=3)
    bordersize=12
    border=cv2.copyMakeBorder(image, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
    border=cv2.copyMakeBorder(border, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[255,255,255] )
    #border = cv2.equalizeHist(border,border)
    #border = cv2.GaussianBlur(border,(3,3),0)
    gray = cv2.cvtColor(border, cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray,gray)

    #gray = cv2.GaussianBlur(gray,(3,3),0)

    (tr1,grayX) = cv2.threshold(gray,150,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    gray1 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,25,3)
    kernel = np.ones((5,5),np.uint8)
    gray1 =cv2.morphologyEx(gray1, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((3,3),np.uint8)
    gray1 = cv2.dilate(gray1,kernel,iterations = 1)
    print (str(tr1))
    #gray = cv2.GaussianBlur(gray,(3,3),0)
    #gray = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh= tr1
    edged = cv2.Canny(gray1, thresh*0.5, thresh)

    image1, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    print (hierarchy)
    ####cnts = sorted(cnts, key = cv2.arcLength, reverse = True)[:50]


    #cv2.drawContours(border, cnts, -1, (255, 0, 255), 3)
    #print (cnts)


    screenCnt = None
    i=0
    for c in cnts:
        #peri = cv2.arcLength(c, True)
        #approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        #cv2.drawContours(border, [c], -1, (255, 255, 0), 1)
        #print ("mam count")
        (tl,bl,tr,br)=find_4_corners(grayX,c)
        print (tl,tr,bl,br)
        #if len(approx) == 4:
        (shY,shX) = border.shape[:2]
        if abs(tl[0]-tr[0])>150 and abs(tl[1]-bl[1])>40 and abs(bl[0]-br[0])>150 and abs(tr[1]-br[1])>40 and abs(tl[0]-tr[0]) < shX-30:

            cv2.drawContours(border, [c], -1, (0, 255, 0), 1)
            rC=c
            print ("mam 1. child")
            #break
        i+=1


    rect = np.zeros((4, 2), dtype = "float32")
    (tl,bl,tr,br)=find_4_corners(border,rC)


    rect[0]=tl
    rect[3]=bl
    rect[2]=br
    rect[1]=tr

    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    shapX= int((abs(tl[0]-tr[0])+abs(bl[0]-br[0]))/2)
    shapY = int((abs(tl[1]-bl[1]) + abs(tr[1]-br[1])) / 2)
    off=24
    dst = np.array([
        [off, off],
        [shapX+off, off],
        [shapX+off, shapY+off],
        [off, shapY+off]], dtype = "float32")




    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (shapX,shapY))

    images=[border,cv2.cvtColor(gray1,cv2.COLOR_GRAY2RGB)]
    height = sum(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = np.zeros((height,width,3))

    y = 0
    for image in images:
        h,w,d = image.shape
        output[y:y+h,0:w] = image
        y += h


    images=[output,cv2.cvtColor(edged,cv2.COLOR_GRAY2RGB)]
    height = sum(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = np.zeros((height,width,3))

    y = 0
    for image in images:
        h,w,d = image.shape
        output[y:y+h,0:w] = image
        y += h

    images=[output,warped]
    height = sum(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = np.zeros((height,width,3))

    y = 0
    for image in images:
        h,w,d = image.shape
        output[y:y+h,0:w] = image
        y += h







    cv2.imwrite('polls/media/correctedTemp/' + (plate.image.name),output)
    corrected=None
    return corrected
