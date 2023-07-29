import cv2
import time,  math, numpy as np
import handTrackMod as htm
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
w, h = pyautogui.size()

detector = htm.handDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()   #(-63.5, 0.0, 0.5) min max

minVol = -63
maxVol = volRange[1]
print(volRange)
hmin = 50
hmax = 200
volBar = 400
volPer = 0
vol = 0
color = (0,215,255)

tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0

pyautogui.FAILSAFE = False
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
   # print(lmList)
    fingers = []

    if len(lmList) != 0:

        #Thumb (play pause)
        if lmList[tipIds[0]][1] > lmList[tipIds[0 - 1]][1]:
            if lmList[tipIds[0]][1] >= lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        elif lmList[tipIds[0]][1] < lmList[tipIds[0 -1]][1]:
            if lmList[tipIds[0]][1] <= lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)


      #  print(fingers)
        if (fingers == [0,0,0,0,0]) & (active == 0 ):
            mode='N'
        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0] or fingers == [0, 1, 1, 1, 0] or fingers == [0, 1, 1, 1, 1]) & (active == 0):
            mode = 'Menu'
            active = 1
        elif (fingers == [1, 1, 0, 0, 0] ) & (active == 0 ):
             mode = 'Volume'
             active = 1
        elif (fingers == [1 ,1 , 1, 1, 1] ) & (active == 0 ):
             mode = 'Music'
             active = 1

############# Menu 👇👇👇👇##############
    if mode == 'Menu':
        active = 1
     #   print(mode)
        putText(mode)
        cv2.rectangle(img, (200, 410), (245, 460), (255, 255, 255), cv2.FILLED)
        if len(lmList) != 0:
            if fingers == [0,1,0,0,0]: #1 finger up
                putText(mode = 'M', loc=(200, 455), color = (0, 255, 0))
                pyautogui.click(1160, 977, 1, 1, button='left')

            if fingers == [0,1,1,0,0]: #2 fingers up
                putText(mode = 'S', loc =  (200, 455), color = (0, 0, 255))
                pyautogui.click(1005, 992, 1, 1, button='left')

            if fingers == [0,1,1,1,0]: #3 fingers up
                putText(mode = 'P', loc =  (200, 455), color = (0, 0, 255))
                pyautogui.click(850, 994, 1, 1, button='left')

            if fingers == [0,1,1,1,1]: #4 fingers up
                putText(mode = 'P', loc =  (200, 455), color = (0, 0, 255))
                pyautogui.click(917, 754, 1, 1, button='left')

            elif fingers == [0, 0, 0, 0, 0]:
                active = 0
                mode = 'N'
################# Volume 👇👇👇####################
    if mode == 'Volume':
        active = 1
       #print(mode)
        putText(mode)
        if len(lmList) != 0:
            if fingers[-1] == 1:
                active = 0
                mode = 'N'
                print(mode)

            else:

                 #   print(lmList[4], lmList[8])
                    x1, y1 = lmList[4][1], lmList[4][2]
                    x2, y2 = lmList[8][1], lmList[8][2]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
                    cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
                    cv2.line(img, (x1, y1), (x2, y2), color, 3)
                    cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)

                    length = math.hypot(x2 - x1, y2 - y1)
                    # print(length)

                    # hand Range 50-300
                    # Volume Range -65 - 0
                    vol = np.interp(length, [hmin, hmax], [minVol, maxVol])
                    volBar = np.interp(vol, [minVol, maxVol], [400, 150])
                    volPer = np.interp(vol, [minVol, maxVol], [0, 100])
                    print(vol)
                    volN = int(vol)
                    if volN % 4 != 0:
                        volN = volN - volN % 4
                        if volN >= 0:
                            volN = 0
                        elif volN <= -64:
                            volN = -64
                        elif vol >= -11:
                            volN = vol

                #    print(int(length), volN)
                    volume.SetMasterVolumeLevel(vol, None)
                    if length < 50:
                        cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)

                    cv2.rectangle(img, (30, 150), (55, 400), (209, 206, 0), 3)
                    cv2.rectangle(img, (30, int(volBar)), (55, 400), (215, 255, 127), cv2.FILLED)
                    cv2.putText(img, f'{int(volPer)}%', (25, 430), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)


#######################################################################
    if mode == 'Music':
        active = 1
        #print(mode)
        putText(mode)
        cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)

        if fingers[1:] == [0,0,0,0]: #thumb excluded
            active = 0
            mode = 'N'
            print(mode)
        else:
            if len(lmList) != 0:
                cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 255, 255), cv2.FILLED) #index
                cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 255, 0), cv2.FILLED)  #thumb
                cv2.circle(img, (lmList[12][1], lmList[12][2]), 10, (255, 165, 0), cv2.FILLED)  # index
                cv2.circle(img, (lmList[16][1], lmList[16][2]), 10, (255, 255, 0), cv2.FILLED)  # ring

                if fingers[0] == 0: #thumb down
                    cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (255, 0, 255), cv2.FILLED)  # thumb
                    pyautogui.click(580, 322, 1, 1, button='left') # accept call
                    print(mode)
                elif fingers[1] == 0: #index down
                    cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 0, 255), cv2.FILLED)  # index
                    pyautogui.press('playpause', interval=0.25)
                elif fingers[2] == 0:  # middle down
                    cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 0, 255), cv2.FILLED)  # mid
                    pyautogui.press('nexttrack', interval=0.25)
                elif fingers[3] == 0: #ring down
                    cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 0, 255), cv2.FILLED)  # ring
                    pyautogui.press('prevtrack', interval=0.25)
                elif fingers[4] == 0: #pinkie down
                    cv2.circle(img, (lmList[8][1], lmList[8][2]), 10, (255, 0, 255), cv2.FILLED)  # pinkie
                    pyautogui.click(1377, 317, 1, 1, button='left')  # decline call


    cTime = time.time()
    fps = 1/((cTime + 0.01)-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}',(480,50), cv2.FONT_ITALIC,1,(255,0,0),2)
    cv2.imshow('Hand LiveFeed',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    def putText(mode,loc = (250, 450), color = (0, 255, 255)):
        cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_PLAIN,
                    3, color, 3)