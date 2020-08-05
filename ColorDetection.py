import argparse
import cv2
import pandas as pd

# creating argparser to read image path from command line
ar=argparse.ArgumentParser()
ar.add_argument("-i","--image",required=True,help="Path of image")
args=ar.parse_args()
imgPath=args.image

#reading image with opencv
img=cv2.imread(imgPath)

#declaring global variables (are used later on)
clicked = False
r = g = b = xpos = ypos = 0

properties=['colorID','colorName','hex','R','G','B']
#reading csv file with pandas
colorData=pd.read_csv('InputData/colors.csv',names=properties,header=None)

def drawFunction(event,x,y,flags,param) :
    if event == cv2.EVENT_LBUTTONDBLCLK :
        global xpos,ypos,b,g,r,clicked
        clicked=True
        xpos=x
        ypos=y
        b,g,r=img[y,x]
        r=int(r)
        g=int(g)
        b=int(b)

def getColorName(R,G,B) :
    min=1000
    for i in range(len(colorData)) :
        d=abs(R-int(colorData.loc[i,'R'])+abs(G-int(colorData.loc[i,'G'])))+abs(B-int(colorData.loc[i,'B']))
        if d<=min :
            min=d
            colorName=colorData.loc[i,'colorName']
    return colorName


cv2.namedWindow('image')
cv2.setMouseCallback('image',drawFunction)

while(True) :
    cv2.imshow('image',img)
    if (clicked) :
        cv2.rectangle(img,(30,30),(600,60),(b,g,r),-1)
        # Creating text string to display ( Color name and RGB values )
        text=getColorName(r,g,b)+' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
        if r+g+b < 350 :
            cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2)
        else :
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2)

        clicked=False

    k=cv2.waitKey(20)
    if k==27 :
        break
cv2.destroyAllWindows()
