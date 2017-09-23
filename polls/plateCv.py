import cv2
import numpy as np


def find_4_corners(border,rC):
    #pre prvy roh
    maxX=0
    minX=10000
    maxY= 0
    minY=10000
    for j in range(0,len(rC)):
        if (rC[j][0][0]<minX and rC[j][0][1]<minY):
            minX=rC[j][0][0]
            minY=rC[j][0][1]

        if (rC[j][0][0]<minX and (abs(rC[j][0][0]-minX) > abs(rC[j][0][1] - minY ))):
            minX=rC[j][0][0]
            minY=rC[j][0][1]

        if (rC[j][0][1]<minY and (abs(rC[j][0][0]-minX) < abs(rC[j][0][1] - minY ))):
            minX=rC[j][0][0]
            minY=rC[j][0][1]

    cv2.circle(border,(minX,minY),10,(0,0,255),2)
    tl=[minX,minY]




    #pre druhy roh
    maxX=0
    minX=10000
    maxY= 0
    minY=10000
    for j in range(0,len(rC)):
        if (rC[j][0][0]<minX and rC[j][0][1]>maxY):
            minX=rC[j][0][0]
            maxY=rC[j][0][1]

        if (rC[j][0][0]<minX and (abs(rC[j][0][0]-minX) > abs(rC[j][0][1] - maxY ))):
            minX=rC[j][0][0]
            maxY=rC[j][0][1]

        if (rC[j][0][1]>maxY and (abs(rC[j][0][0]-minX) < abs(rC[j][0][1] - maxY ))):
            minX=rC[j][0][0]
            maxY=rC[j][0][1]

    cv2.circle(border,(minX,maxY),10,(255,0,255),2)
    tr=[minX,maxY]





        #pre treti roh
    maxX=0
    minY=10000
    for j in range(0,len(rC)):
        if (rC[j][0][0]>maxX and rC[j][0][1]<minY):
            maxX=rC[j][0][0]
            minY=rC[j][0][1]

        if (rC[j][0][1]<minY and (abs(rC[j][0][1]-minY) > abs(rC[j][0][0] - maxX ))):
            maxX=rC[j][0][0]
            minY=rC[j][0][1]

        if (rC[j][0][0]>maxX and (abs(rC[j][0][1]-minY) < abs(rC[j][0][0] - maxX ))):
            maxX=rC[j][0][0]
            minY=rC[j][0][1]
    cv2.circle(border,(maxX,minY),10,(0,255,255),2)
    bl=[maxX,minY]








            #pre stvrty roh
    maxX=0
    minX=10000
    maxY= 0
    minY=10000
    for j in range(0,len(rC)):
        if (rC[j][0][0] > maxX and rC[j][0][1] > maxY):
            maxX=rC[j][0][0]
            maxY=rC[j][0][1]

        if (rC[j][0][0] > maxX and (abs(rC[j][0][0]-maxX) > abs(rC[j][0][1] - maxY ))):
            maxX=rC[j][0][0]
            maxY=rC[j][0][1]

        if (rC[j][0][1] > maxY and (abs(rC[j][0][0] - maxX) < abs(rC[j][0][1] - maxY ))):
            maxX=rC[j][0][0]
            maxY=rC[j][0][1]

    cv2.circle(border,(maxX,maxY),10,(0,0,255),2)
    br=[maxX,maxY]

    return [tl,tr,bl,br]

def correctPlate(plate):
    imageIo = cv2.imread('polls/' + (plate.image.url))
    imageI = cv2.resize(imageIo, (0,0), fx=5, fy=5)
    bordersize=12
    border=cv2.copyMakeBorder(imageI, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[0,0,0] )
    border=cv2.copyMakeBorder(border, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType= cv2.BORDER_CONSTANT, value=[255,255,255] )

    gray = cv2.cvtColor(border, cv2.COLOR_BGR2GRAY)

    (tr1,grayX) = cv2.threshold(gray,150,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    gray1 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,25,3)
    kernel = np.ones((5,5),np.uint8)
    gray1 =cv2.morphologyEx(gray1, cv2.MORPH_OPEN, kernel)
    kernel = np.ones((3,3),np.uint8)
    gray1 = cv2.dilate(gray1,kernel,iterations = 1)

    thresh= tr1
    edged = cv2.Canny(gray1, thresh*0.5, thresh)

    image1, cnts, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)



    nemam = True
    i=0
    for c in cnts:

        (tl,bl,tr,br)=find_4_corners(grayX,c)

        (shY,shX) = border.shape[:2]

        if abs(tl[0]-tr[0])>150 and abs(tl[1]-bl[1])>40 and abs(bl[0]-br[0])>150 and abs(tr[1]-br[1])>40 and abs(tl[0]-tr[0]) < shX-30:

            cv2.drawContours(border, [c], -1, (0, 255, 0), 1)
            rC=c
            nemam=False
            break

        i+=1



    if nemam:
        images=[border,cv2.cvtColor(gray1,cv2.COLOR_GRAY2RGB)]
        height = sum(image.shape[0] for image in images)
        width = max(image.shape[1] for image in images)
        output = np.zeros((height,width,3), dtype = "float32")

        y = 0
        for image in images:
            h,w,d = image.shape
            output[y:y+h,0:w] = image
            y += h


        images=[output,cv2.cvtColor(edged,cv2.COLOR_GRAY2RGB)]
        height = sum(image.shape[0] for image in images)
        width = max(image.shape[1] for image in images)
        output = np.zeros((height,width,3), dtype = "float32")

        y = 0
        for image in images:
            h,w,d = image.shape
            output[y:y+h,0:w] = image
            y += h

        #cv2.imwrite('polls/media/correctedTemp/' + (plate.image.name),output)
        cv2.imwrite('polls/media/correctedTemp/' + (plate.image.name),imageIo)
        corrected=str('polls/media/correctedTemp/' + (plate.image.name))
        return corrected


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
    warped = cv2.warpPerspective(imageI, M, (shapX,shapY))

    images=[border,cv2.cvtColor(gray1,cv2.COLOR_GRAY2RGB)]
    height = sum(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = np.zeros((height,width,3), dtype = "float32")

    y = 0
    for image in images:
        h,w,d = image.shape
        output[y:y+h,0:w] = image
        y += h


    images=[output,cv2.cvtColor(edged,cv2.COLOR_GRAY2RGB)]
    height = sum(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = np.zeros((height,width,3), dtype = "float32")

    y = 0
    for image in images:
        h,w,d = image.shape
        output[y:y+h,0:w] = image
        y += h

    images=[output,warped]
    height = sum(image.shape[0] for image in images)
    width = max(image.shape[1] for image in images)
    output = np.zeros((height,width,3), dtype = "float32")

    y = 0
    for image in images:
        h,w,d = image.shape
        output[y:y+h,0:w] = image
        y += h

    warped= cv2.resize(warped, (0,0), fx=0.2, fy=0.2)

    cv2.imwrite('polls/media/correctedTemp/' + (plate.image.name),warped)
    #cv2.imwrite('polls/media/correctedTemp/' + (plate.image.name),output)
    corrected=str('polls/media/correctedTemp/' + (plate.image.name))
    return corrected
