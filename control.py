import cv2
from collections import Counter
from module import findnameoflandmark,findpostion
import math
import os
from time import *
from pynput.keyboard import Key, Controller
import subprocess
import time

keyboard = Controller()
cap = cv2.VideoCapture(0)
cap.set(3, 128)
cap.set(4, 128) 
tip=[8,12,16,20]
tipname=[8,12,16,20]
fingers=[]
finger=[]

while True:

     ret, frame = cap.read()
     #flipped = cv2.flip(frame, flipCode = -1)
     frame1 = cv2.resize(frame, (160, 75))
     
         
     a=findpostion(frame1)
     b=findnameoflandmark(frame1 )
         
     
     if len(b and a)!=0:
        finger=[]
        if a[0][1:] < a[4][1:]: 
           finger.append(1)
           print (b[4])
                               
        else:
           finger.append(0)     
        
        fingers=[] 
        for id in range(0,4):
            if a[tip[id]][2:] < a[tip[id]-2][2:]:      
               print(b[tipname[id]])
               fingers.append(1)
            else:
               fingers.append(0)
                        
     x=fingers + finger
     c=Counter(x)
     up=c[1]
     down=c[0]
     #print(up)
     #print(down)
     
     cv2.imshow("Frame", frame1);
     key = cv2.waitKey(1) & 0xFF
     
     if up == 5:
         keyboard.press('s')
         keyboard.release('s')
     
     if up == 4:
        keyboard.press('a')
        keyboard.release('a')
        
     if up == 3:   
        keyboard.press('n')
        keyboard.release('n')
     
     if up == 2:         
        volume = 100
        command = ["amixer", "sset", "Master", "{}%".format(volume)]
        subprocess.Popen(command)
     
     if up == 1:
        volume = 0
        command = ["amixer", "sset", "Master", "{}%".format(volume)]
        subprocess.Popen(command)
        
    if up == 0:
        print("N")

