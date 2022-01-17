# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:24:38 2021

@author: EFE
"""

import cv2
import numpy as np
from collections import deque

# nesne merkezini depolayacak veri tipi
buffer_size = 16
pts = deque(maxlen = buffer_size)


# capture
video = cv2.VideoCapture(0)
video.set(3,640)
video.set(4,480)


def empty(a):
    pass


cv2.namedWindow("trackbar")   
cv2.resizeWindow("trackbar", 640, 480)
h_max = cv2.createTrackbar("h_max", "trackbar", 0, 255, empty)
h_min = cv2.createTrackbar("h_min", "trackbar", 0, 255, empty)
s_max = cv2.createTrackbar("s_max", "trackbar", 0, 255, empty)
s_min = cv2.createTrackbar("s_min", "trackbar", 0, 255, empty)
v_max = cv2.createTrackbar("v_max", "trackbar", 0, 255, empty)
v_min = cv2.createTrackbar("v_min", "trackbar", 0, 255, empty)

erode = cv2.createTrackbar("erode", "trackbar", 0, 50, empty)
dilate = cv2.createTrackbar("dilate", "trackbar", 0, 50, empty)

dilate = 2
erode = 2


while True:
    
    success, imgOriginal = video.read()
    
    if success: 
        
                
        yatay_cizgiler = [0,120,240,360,480,640]
        dikey_cizgiler = [0,160,320,480]
        
        for i in yatay_cizgiler:
            orijinal = cv2.line(imgOriginal, (0,i), (640,i), (250,0,75), 1)
        for i in dikey_cizgiler:
            orijinal = cv2.line(imgOriginal, (i,0), (i,480), (130,0,75), 1)
        
        
        # blur
        blurred = cv2.GaussianBlur(imgOriginal, (11,11), 0) 
        
        # hsv
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        
        
        h_max = cv2.getTrackbarPos("h_max", "trackbar")
        h_min = cv2.getTrackbarPos("h_min", "trackbar")
        s_max = cv2.getTrackbarPos("s_max", "trackbar")
        s_min = cv2.getTrackbarPos("s_min", "trackbar")
        v_max = cv2.getTrackbarPos("v_max", "trackbar")
        v_min = cv2.getTrackbarPos("v_min", "trackbar")
        
        erode = cv2.getTrackbarPos("erode", "trackbar")
        dilate = cv2.getTrackbarPos("dilate", "trackbar")
    
        
        Lower = np.array([h_min, s_min, v_min])
        Upper = np.array([h_max, s_max, v_max])
        
        
        
        
        
        mask1 = cv2.inRange(hsv, (80,39,0), (255,139,106)) #renk için maskeleme
        mask2 = cv2.inRange(hsv, Lower, Upper) #renk için maskeleme
        
        mask = mask1 + mask2
        
        
        # maskenin etrafında kalan gürültüleri sil
        mask = cv2.erode(mask, None, iterations = erode)    # maskenin etrafında kalan gürültüleri sil 
        mask = cv2.dilate(mask, None, iterations = dilate)  # maskenin etrafında kalan gürültüleri sil    
        
        
        
        
        cv2.imshow("Mask + erozyon ve genisleme",mask)
        
    
        # kontur
        (contours,_) = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        if len(contours) > 0:
            
            # en buyuk konturu al
            c = max(contours, key = cv2.contourArea)
            
            rect = cv2.minAreaRect(c)
            
            ((x,y), (width,height), rotation) = rect
            
            s = "x: {}, y: {}, width: {}, height: {}, rotation: {}".format(np.round(x),np.round(y),np.round(width),np.round(height),np.round(rotation))
            print(s)
           
            
            if int(x) < int(dikey_cizgiler[1]) and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(imgOriginal, "koordinat 1-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-1")
            elif int(x) < int(dikey_cizgiler[1]) and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(imgOriginal, "koordinat 1-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-2")
            elif int(x) < int(dikey_cizgiler[1]) and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(imgOriginal, "koordinat 1-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-3")
            elif int(x) < int(dikey_cizgiler[1]) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(imgOriginal, "koordinat 1-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-4")
                           
            # koordinat 2-1 2-2 2-3 2-4 
            if  int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2]) and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(imgOriginal, "koordinat 2-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-1")
            elif int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2])and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(imgOriginal, "koordinat 2-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-2")
            elif int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2])and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(imgOriginal, "koordinat 2-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-3")
            elif int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2]) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(imgOriginal, "koordinat 2-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-4")
                    
            # koordinat 3-1 3-2 3-3 3-4 
            if int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(imgOriginal, "koordinat 3-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-1")
            elif int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(imgOriginal, "koordinat 3-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-2")
            elif int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(imgOriginal, "koordinat 3-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-3")
            elif int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(imgOriginal, "koordinat 3-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-4")
                         
            # koordinat 4-1 4-2 4-3 4-4 
            if int(dikey_cizgiler[3]) < int(x)  and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(imgOriginal, "koordinat 4-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-1")
            elif int(dikey_cizgiler[3]) < int(x)  and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(imgOriginal, "koordinat 4-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-2")
            elif int(dikey_cizgiler[3]) < int(x)  and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(imgOriginal, "koordinat 4-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-3")
            elif int(dikey_cizgiler[3]) < int(x) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(imgOriginal, "koordinat 4-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-4")
            
           
            
           
            
           
            
           
            
           
            
           
            
            # kutucuk
            box = cv2.boxPoints(rect)
            box = np.int64(box)
            
            # moment
            M = cv2.moments(c)
            if M["m00"] != 0:                                                    #----\
                center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))        #     \ Bu kısım düzenlenecek.
            else:                                                                #     / center(0,0) yerine kameraya yeniden bağlanacak.
                center = None                                                 #____/ 
                
            # konturu çizdir
            cv2.circle(imgOriginal, center, 50, (0,255,0),2)
            
            # merkere bir tane nokta çizelim
            cv2.circle(imgOriginal, center, 5, (25,0,255),-1)
            
            # bilgileri ekrana yazdır
            cv2.putText(imgOriginal, s, (25,50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 2)
        elif len(contours)<=0:
            pass
    
            
        pts.appendleft(center)
        for i in range(1, len(pts)):
            
            if pts[i-1] is None or pts[i] is None: continue
        
            cv2.line(imgOriginal, pts[i-1], pts[i],(0,255,0),3) # 
            
        cv2.imshow("Orijinal Tespit",orijinal)
        
        
        
        if cv2.waitKey(1) & 0xFF == ord("q"): 
            cv2.destroyAllWindows()
            cap.release() 
            break

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
