import cv2
from collections import Counter
from module import findnameoflandmark,findpostion,speak
import math

cap = cv2.VideoCapture(0) #video stream
tip=[8,12,16,20] #tip IDS
tipname=[8,12,16,20] 
fingers=[] #FINGER ARRAY
finger=[] #SELECTED FINGER ARRAY

while True:
     ret, frame = cap.read() 
     
     #Frame Size
     frame1 = cv2.resize(frame, (320, 200))
    
    #Location of the joints of the fingers 
     a=findpostion(frame1)
     b=findnameoflandmark(frame1)
     
     #determine if finger is up or down
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
     #print finger up or down        
     x=fingers + finger
     c=Counter(x)
     up=c[1]
     down=c[0]
     print('This many fingers are up - ', up)
     print('This many fingers are down - ', down)
     
     #Current frame to the desktop 
     cv2.imshow("Frame", frame1);
     key = cv2.waitKey(1) & 0xFF
     
     #s key to stop
     if key == ord("s"):
       break

