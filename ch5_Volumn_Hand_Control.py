import cv2
import time
import numpy as np
import math
import ch1_HandTracking as HT
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#####################
vcam,hcam=640,480
#####################

cap= cv2.VideoCapture(0)
cap.set(3,vcam)
cap.set(4,hcam)

pTime=0
detector=HT.HandDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-20, None)
minVol=volRange[0]
maxVol=volRange[1]
volBar=400
vol=0
volPer=0
while True:
    success,img=cap.read()
    img=cv2.flip(img,1)
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList) !=0:
        # print(lmList[4],lmList[8])
        
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        length=math.hypot(x2-x1,y2-y1)
        # print(length)
        
        # Hand Range = 20 - 180
        # Volumn Range = -65 - 0 
        
        vol=np.interp(length,[20,180],[minVol,maxVol])
        volBar=np.interp(length,[20,180],[200,400])
        volPer=np.interp(length,[20,180],[0,100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)


        if length<=30:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)
    
    cv2.rectangle(img, (30,200), (65,400),(0,255,0),3)
    cv2.rectangle(img,(30,200),(65,int(volBar)),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)}',(70,440),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),3) 
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'fps:{int(fps)}',(70,50),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3) 
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break