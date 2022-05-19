import cv2
import mediapipe as mp
import time
import os
import random
import tkinter as tk
import HandTrackingModule as hm

def popup(msg):
    popup = tk.Tk()
    popup.wm_title("Result")
    popup.geometry("500x100")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1= tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
detector = hm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
count_down = 0
player = -1

end = time.time() + 5
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
            
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    string = ""
    #frame
    # cv2.putText(img, str(int(fps)), (10,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 2)

    if len(lmList) != 0:
        fingers = []

        #thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        #4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        if fingers.count(1) == 0:
            string = "You are playing Rock"
            player = 0
        elif fingers.count(1) == 2 and ((fingers[0] == 1 and fingers[1] == 1) or (fingers[1] == 1 and fingers[2] == 1)):
            string = "You are playing Scissors"
            player = 1
        elif fingers.count(1) == 5:
            string = "You are playing Paper"
            player = 2
    

    if cTime > end:
        break
    else:
        cv2.putText(img, "You have " + str(int(abs(cTime-end))) + " seconds left", (20, 400), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)            
    cv2.putText(img, string, (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)

    count_down += 1

    cv2.imshow("Image", img)
    cv2.waitKey(1)

AI_choose = random.randint(0,2)

if player == AI_choose:
    popup("It's a draw!")

elif player == 0:
    if AI_choose == 1:
        popup("Bot played Scissors, You WIN! :)")
    elif AI_choose == 2:
        popup("Bot played Paper, You LOSE :(")

elif player == 1:
    if AI_choose == 0:
        popup("Bot played Rock, You LOSE :(")
    elif AI_choose == 2:
        popup("Bot played Paper, You WIN! :)")

elif player == 2:
    if AI_choose == 0:
        popup("Bot played Rock, You WIN! :)")
    elif AI_choose == 1:
        popup("Bot played Scissors, You LOSE :(")

else:
    popup("You did not play anything or We could not detect your move")