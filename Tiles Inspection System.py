import cv2
import numpy as np
import tkinter as tk
from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkinter import scrolledtext
import time
import os

#============================================================================================================================================================
#Functionality

def Destroy():
    root.destroy()
    cap.release()
    cv2.destroyAllWindows()

def slider_changed(value):
    threshold_value = float(value)
    

#============================================================================================================================================================

#GUI Section

root=Tk()
root.title("Ceramic Tiles Quality Inspection System")
root.geometry("1300x870")
#root.wm_iconbitmap("E:\FYP\Template Matching\GUIs\icon.ico")
#bgImage=ImageTk.PhotoImage(file='E:\FYP\Interface(fyp)\Home.png')

#bgLabel=Label(root,image=bgImage)
#bgLabel.pack()
root.configure(bg="azure4")
Label(root,text="CERAMIC TILES QUALITY INSPECTION SYSTEM",font=("Algerian",37,"bold"),bg="azure4",fg="gray15").pack()

#Frame1=Frame(root,width=1070,height=1,bg='white')
#Frame1.place(x=110,y=50)


fr=LabelFrame(root,bg="white")
fr.pack()
la=Label(fr,bg="white")
la.pack(side=LEFT)

fr1=LabelFrame(root,bg="white")
fr1.pack()
la1=Label(fr,bg="white")
la1.pack(side=tk.RIGHT)


Frame3=Frame(root,width=303,height=80,bg='gray15')
Frame3.place(x=40,y=560)

text2=Label(root,text="Thresholding",font=("Bookman Old Style",12,"bold"),bg="gray15",fg="white")
text2.place(x=43,y=565)

#Frame4=Frame(root,width=350,height=80,bg='gray15')
#Frame4.place(x=345,y=560)

#text3=Label(root,text="Zoom Control",font=("Bookman Old Style",12,"bold"),bg="gray15",fg="white")
#text3.place(x=370,y=565)

#Frame4=Frame(root,width=5,height=80,bg='white')
#Frame4.place(x=360,y=560)

#threshold_value=120

#Drop Down Menu
clicked= StringVar()
#clicked.set("Original Video")

drop=OptionMenu(root, clicked, "Original Video", "Gray Scale", "Thresholding", "Invert Image")
drop.place(x=1,y=1)

#Slider
scale_int = tk.IntVar(value=127)
scale=tk.Scale(root, command=lambda value: print(int(scale_int.get())),
                from_=0, to=230,
                length=295,
                orient="horizontal",
                variable = scale_int,bg="gray")

#scale.set(threshold_value)
scale.place(x=41,y=590)


#scale_int1 = tk.IntVar(value=140)
#scale=tk.Scale(root, command=lambda value: print(int(scale_int1.get())),
#                from_=0, to=255,
#                length=300,
#                orient="horizontal",
#                variable = scale_int1)

#scale.set(threshold_value)
#scale.place(x=370,y=590)


#thresh = tk.Label(root, text=str(m))
#thresh.place(x=850,y=600)

thresh1 = tk.Label(root, text="Accuracy")
thresh1.place(x=658,y=500)


#End=ImageTk.PhotoImage(file='E:\FYP\Interface(fyp)\exit.jpg')
#End1=Button(root,image=End,bd=0,fg='black',activeforeground='black',bg='Black',cursor='hand2',command=Destroy)

button1=Button(root,text='Exit',font=('Bookman Old Style',20,'bold'),
               bd=0,bg='gray15',fg='white',cursor='hand2',
               command=Destroy,activeforeground='gray25')
button1.place(x=1100,y=580)

text=Label(root,text="Original Frame",font=("Broadway",15,"bold"),bg="azure4",fg="gray15")
text.place(x=220,y=525)

Frame2=Frame(root,width=190,height=1,bg='gray15')
Frame2.place(x=218,y=550)

text1=Label(root,text="Defect Detection Frame",font=("Broadway",15,"bold"),bg="azure4",fg="gray15")
text1.place(x=800,y=525)

Frame2=Frame(root,width=285,height=1,bg='gray15')
Frame2.place(x=798,y=550)

#============================================================================================================================================================

#Template Calling
template_directory="E:\FYP\Template Matching\Spot Dataset"
template_files = [os.path.join(template_directory, filename) for filename in os.listdir(template_directory) if filename.endswith(('.jpg', '.png', '.jpeg'))]

# Initialize an empty list to store template images
templates = []

# Load all template images
for template_file in template_files:
    template = cv2.resize(cv2.imread(template_file,cv2.IMREAD_GRAYSCALE), (0, 0), fx=0.95, fy=0.95)
    if template is not None:
        templates.append(template)
    else:
        print(f"Unable to read template image: {template_file}")

#============================================================================================================================================================

#Processing Section

#Capturing Live Video
cap=cv2.VideoCapture(1)

while True:

    img=cap.read()[1]
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    resize1 = cv2.resize(img, (0, 0), fx = 0.95, fy = 0.95)

    #Converting Image into Gray
    grey= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resize = cv2.resize(grey, (0, 0), fx = 0.95, fy = 0.95)
    
    #Converting Image into binary
    _, threshold = cv2.threshold(resize, scale_int.get(), 255, cv2.THRESH_BINARY)
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
        #print(max_val*100,min_val*100)
        m=round(max_val*100,0)
        #thresh = tk.Label(root, text=(str(m),"%"))
        #thresh.place(x=850,y=600)
        loc2 = np.where(result >= 0.7)
        for pt in zip(*loc2[::-1]):
            cv2.rectangle(invert, pt, (pt[0] + w+3, pt[1] + h+2), 255, 0)
            cv2.putText(invert, "X", (pt[0] + w-16, (pt[1] + h) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3, 255, 1)
            cv2.putText(invert,"Accuracy",(20, 50), 1, 1, (255, 255, 0))
            cv2.putText(invert,"%",(60, 70), 1, 1, (255, 255, 0))
            cv2.putText(invert,str(m),(20, 70), 1, 1, (255, 255, 0))

        if m>70:
            thresh = tk.Label(root, text=(str(m),"%"))
            thresh.place(x=712,y=500)

    # Find contours
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area (adjust the threshold as needed)
    min_contour_area = 10000
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

    # Draw bounding boxes around the detected edges and write text
    #frame_with_edges = resize1.copy()
    for idx, cnt in enumerate(filtered_contours):
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        hull = cv2.convexHull(approx)

        if len(approx) != 4:
            cv2.drawContours(resize1, [approx], -1, (0, 255, 0), 2)
            cv2.putText(resize1, 'Defected', tuple(approx[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            
        # Draw bounding box
        cv2.drawContours(resize1, [hull], 0, (0, 0, 255), 2)

        # Write text on the defected area
        cv2.putText(resize1, ' ', tuple(hull[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
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

    


