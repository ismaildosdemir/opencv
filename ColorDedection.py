# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 23:15:14 2021

@author: EFE
"""

import cv2
import numpy as np
from collections import deque

 
# nesne merkezi depolamak için kullanılır
buffer_size = 16
points = deque(maxlen = buffer_size)

# MAVİ RENGİNİN TESPİTİ --- RENK ARALIĞI HESAPLANIR ---
mavi_lower = (84, 98, 0)
mavi_upper = (179, 255, 255)

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# genislik
cap.set(3,640)
# yukseklik
cap.set(4, 480)


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(" Kamera Genslik: ", width, " Kamera Yukseklik: ", height)

while True : 

    success, video = cap.read()
    cv2.circle(video, (319,239), 2, (0,0,255), cv2.FILLED)
    # bu yüzden 
    if success:
        
        ## alan ayırmak için kullanılan mor çizgiler --- dizi kullanılır..
        yatay_cizgiler = [0,120,240,360,480,640]
        dikey_cizgiler = [0,160,320,480]
        
        for i in yatay_cizgiler:
            cv2.line(video, (0,i), (640,i), (250,0,75), 1)
        for i in dikey_cizgiler:
            cv2.line(video, (i,0), (i,480), (130,0,75), 1)
        ## alan ayırmak için kullanılan mor çizgiler ---
        
    
        # blur
        # blur yaparak detaylarımızı azaltırız 
        # imgorj kullanılır - pencere boyutu - standart sapma 
        # kamera çalışmıyor hatası alırız img boş olursa 
                                    # pencere boyutu, standart sapma
        blurred = cv2.GaussianBlur(video, (11,11), 0)
            
        # hsv
                                # bgr den hsv çevrime
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        # cv2.imshow("HSV", hsv)
        
        # mavi için maske oluştur
        mask = cv2.inRange(hsv, mavi_lower, mavi_upper)
        # erezyon ve genişleme iteration erozyonun kaç kere uygulanması gerektiğidir
        mask = cv2.erode(mask, None, iterations = 3)
        mask = cv2.dilate(mask, None, iterations = 3)
        #cv2.imshow("MASK", mask)
        
        # kontur
        conturs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None
        
        cv2.putText(video, "MERKEZ ", (290,230), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (130,0,70),1)
        
        if len(conturs) > 0:
             # en buyuk konturu al
            c = max(conturs, key = cv2.contourArea)
            
            # daireye çevir 
            rect = cv2.minAreaRect(c)
            
            (x, y), radius = cv2.minEnclosingCircle(c)
            
            
            s = "x noktasi: {}, y noktasi: {}, rotation: {}".format(np.round(x),np.round(y),np.round(radius))
            print(s)
            
            
            uzaklik = "x merkeze uzaklik: {}, y merkeze uzaklik: {}, rotation: {}".format(320 - np.round(x), 240 - np.round(y),np.round(radius))
            print(uzaklik)
            
            """
            https://www.unitconverters.net/typography/pixel-x-to-centimeter.htm
            
            """
            
            # dışına çizgi çiz
            center = (int(x), int(y))
            radius = int(radius)
            
            """
            yatay_cizgiler = [0,120,240,360,480,640]
            dikey_cizgiler = [0,160,320,480]
            """
            
            # koordinat 1-1 1-2 1-3 1-4 
            if int(x) < int(dikey_cizgiler[1]) and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(video, "koordinat 1-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-1")
            elif int(x) < int(dikey_cizgiler[1]) and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(video, "koordinat 1-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-2")
            elif int(x) < int(dikey_cizgiler[1]) and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(video, "koordinat 1-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-3")
            elif int(x) < int(dikey_cizgiler[1]) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(video, "koordinat 1-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 1-4")
                           
            # koordinat 2-1 2-2 2-3 2-4 
            if  int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2]) and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(video, "koordinat 2-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-1")
            elif int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2])and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(video, "koordinat 2-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-2")
            elif int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2])and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(video, "koordinat 2-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-3")
            elif int(dikey_cizgiler[1]) < int(x) < int(dikey_cizgiler[2]) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(video, "koordinat 2-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 2-4")
                    
            # koordinat 3-1 3-2 3-3 3-4 
            if int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(video, "koordinat 3-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-1")
            elif int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(video, "koordinat 3-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-2")
            elif int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(video, "koordinat 3-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-3")
            elif int(dikey_cizgiler[2]) < int(x) < int(dikey_cizgiler[3]) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(video, "koordinat 3-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 3-4")
                         
            # koordinat 4-1 4-2 4-3 4-4 
            if int(dikey_cizgiler[3]) < int(x)  and int(y) < int(yatay_cizgiler[1]) :
                cv2.putText(video, "koordinat 4-1", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-1")
            elif int(dikey_cizgiler[3]) < int(x)  and int(yatay_cizgiler[1])  < int(y) < int(yatay_cizgiler[2]) :
                cv2.putText(video, "koordinat 4-2", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-2")
            elif int(dikey_cizgiler[3]) < int(x)  and int(yatay_cizgiler[2])  < int(y) < int(yatay_cizgiler[3]) :
                cv2.putText(video, "koordinat 4-3", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-3")
            elif int(dikey_cizgiler[3]) < int(x) and int(yatay_cizgiler[3])  < int(y) < int(yatay_cizgiler[4]) :
                cv2.putText(video, "koordinat 4-4", (15,380), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250,250,250), 1)
                print("koordinat 4-4")
   
                
            #mavi alanın orta noktası
            # merkeze bir tane nokta çizelim: yeşil
            cv2.circle(video, center, 3, (0, 255, 0), -1)
            
            
            # merkez noktası koordinat sorgu
            cv2.circle(video, center, 3, (0, 255, 0), -1)
        
                
  
            # merkez ile nesne merkerzi arasına çizgi ekleme
            # (resim, başlangıç noktası, bitiş noktası, renk, kalınlık)
            cv2.line(video, center, (319,239), (0,0,255), 1) # BGR = (0,255,0)


            cv2.circle(video, center, radius, (0, 0, 255), 2)
            # bilgileri ekrana yazdır
            cv2.putText(video, s, (15,405), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            cv2.putText(video, uzaklik, (15,430), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
            # cv2.putText(video, uzaklik_cm, (15,455), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

        cv2.imshow("merkez noktali", video)
            
            
        if cv2.waitKey(1) & 0xFF == ord("q"): 
            cv2.destroyAllWindows()
            cap.release() # işlemleri serbest bırakırız
            break

    
    
