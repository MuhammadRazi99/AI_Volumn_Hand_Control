import cv2
import time
import mediapipe as mp
from pip import main

class HandDetector():
    def __init__(self,mode=False, maxHands=2, detectionCon=0.5, trackingCon=0.5):
        self.mode= mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackingCon=trackingCon
        
        self.mphands= mp.solutions.hands
        self.hands=self.mphands.Hands(self.mode, self.maxHands, 1,self.detectionCon,self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]
    
    def findHands(self, img, draw=True ):
        imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.result=self.hands.process(imgRGB)
        # print(result.multi_hand_landmarks)
        
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mphands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        self.lmList=[]
        if self.result.multi_hand_landmarks:
            myHand=self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c=img.shape
                cx,cy=int(lm.x*w), int(lm.y*h)
                # print(id,cx,cy)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED)
        
        return self.lmList
    def fingersUp(self):
        fingers=[]
        if len(self.lmList)!=0:
        # Thumb
            if self.lmList[self.tipIds[0]][1]<self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        # 4 fingers
            for id in range(1,5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            return fingers
def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # width
    cap.set(4, 480)  # height
    cap.set(10, 100) # brightness
    cTime = 0
    pTime = 0
    detector=HandDetector()
    while True:
        success, img= cap.read()
        img=detector.findHands(img)
        lmList=detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            print(lmList[4])

        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2 )
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__=="__main__":
    main()