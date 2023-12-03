import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import time
import os

#============================================================================================================================================================
#Functionality

def Destroy():
    root.destroy()
    cv2.destroyAllWindows()

#============================================================================================================================================================

#GUI

root=Tk()
root.geometry("1300x870")
#bgImage=ImageTk.PhotoImage(file='E:\FYP\Interface(fyp)\Home.png')

#bgLabel=Label(root,image=bgImage)
#bgLabel.pack()
root.configure(bg="black")
Label(root,text="CERAMIC TILES QUALITY INSPECTION SYSTEM",font=("Algerian",37,"bold"),bg="black",fg="Light Green").pack()

fr=LabelFrame(root,bg="white")
fr.pack()
la=Label(fr,bg="white")
la.pack(side=tk.LEFT)

fr1=LabelFrame(root,bg="white")
fr1.pack()
la1=Label(fr,bg="white")
la1.pack(side=tk.RIGHT)


End=ImageTk.PhotoImage(file='E:\FYP\Interface(fyp)\exit.jpg')
End1=Button(root,image=End,bd=0,fg='black',activeforeground='black',bg='Black',cursor='hand2',command=Destroy)
End1.place(x=1080,y=550)

text=Label(root,text="Original Frame",font=("Bookman Old Style",20,"bold"),bg="black",fg="Light Green")
text.place(x=80,y=510)

text=Label(root,text="Defect Detection Frame",font=("Bookman Old Style",20,"bold"),bg="black",fg="Light Green")
text.place(x=650,y=510)
#============================================================================================================================================================

#Template Calling
template_directory="E:\FYP\Template Matching\Spot Dataset"
template_files = [os.path.join(template_directory, filename) for filename in os.listdir(template_directory) if filename.endswith(('.jpg', '.png', '.jpeg'))]

# Initialize an empty list to store template images
templates = []

# Load all template images
for template_file in template_files:
    template = cv2.resize(cv2.imread(template_file,cv2.IMREAD_GRAYSCALE), (0, 0), fx=0.9, fy=0.9)
    if template is not None:
        templates.append(template)
    else:
        print(f"Unable to read template image: {template_file}")

#============================================================================================================================================================

#Processing

#Capturing Live Video
cap=cv2.VideoCapture(0)

while True:

    img=cap.read()[1]
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    resize1 = cv2.resize(img, (0, 0), fx = 0.9, fy = 0.9)

    #Converting Image into Gray
    grey= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resize = cv2.resize(grey, (0, 0), fx = 0.9, fy = 0.9)

    #Converting Image into binary
    _, threshold = cv2.threshold(resize, 120, 255, cv2.THRESH_BINARY)
    _, threshold2 = cv2.threshold(template, 140, 255, cv2.THRESH_BINARY)

    #Inverting image
    invert = cv2.bitwise_not(threshold)
    invert2 = cv2.bitwise_not(threshold2)

    #Size of dataset
    h, w = template.shape[::-1]
    
    #Methods from template matching
    methods = [cv2.TM_CCOEFF_NORMED,
            cv2.TM_CCORR_NORMED]

    #Template Matching Algorithm
    for method in methods:
        result = cv2.matchTemplate(invert, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print(max_val*100,min_val*100)
        m=round(max_val*100,0)
        loc2 = np.where(result >= 0.7)
        for pt in zip(*loc2[::-1]):
            cv2.rectangle(invert, pt, (pt[0] + w+3, pt[1] + h+2), 255, 0)
            cv2.putText(invert, "X", (pt[0] + w-16, (pt[1] + h) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1)
            cv2.putText(invert,"Accuracy",(20, 50), 1, 1, (255, 255, 0))
            cv2.putText(invert,"%",(60, 70), 1, 1, (255, 255, 0))
            cv2.putText(invert,str(m),(20, 70), 1, 1, (255, 255, 0))

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    tile_contours = [contour for contour in contours if 1000 <= cv2.contourArea(contour) <= 50000]

    # Draw the filtered contours on the original image
    cv2.drawContours(resize1, tile_contours, -1, (0, 255, 0), 2)

    # Display the original image with the detected tiles
    #cv2.imshow('Detected Tiles', framer)
    #cv2.imwrite("E:\FYP\Template Matching\DefectDetectionSpot1\defect_detection%d.jpg" % count,hor)
    key=cv2.waitKey(1)
    if key == 27:
        break
    elif key==ord('f'):
        cv2.imwrite("E:\FYP\Template Matching\DefectDetectionSpot1\opencv_frame%d.jpg" % count,hor)
        count += 1


    
    
    #hor=np.hstack((resize,grey))


    #Original frame
    img1=ImageTk.PhotoImage(Image.fromarray(resize1))
    la['image']=img1


    #Defect detection Frame
    img=ImageTk.PhotoImage(Image.fromarray(invert))
    la1['image']=img


    root.update()

    


