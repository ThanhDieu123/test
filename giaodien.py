from tkinter import *
import tkinter	
import cv2
from tkinter.ttk import *
import PIL.Image,PIL.ImageTk
import tkinter.filedialog as fd
import os
import winsound
import argparse
import shapely  
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from twilio.rest import Client    
from ultralytics import YOLO
import supervision as sv
import numpy as np
import imutils
from playsound import playsound
import datetime
from time import strftime
import threading
from threading import Thread
import telegram
import time
window=Tk()
window.geometry("800x600")
window.title("TO GIA BAO x NGUYEN THI THANH DIEU")
f=None
points=[]
photo=None


model = YOLO("yolov8s.pt")
def layfile():
	global window, cap,canvas
	f=fd.askopenfilename(parent=window,initialdir=os.getcwd(),title="chọn file")
	cap=cv2.VideoCapture(f)
	canvas_w=cap.get(cv2.CAP_PROP_FRAME_WIDTH)//2
	canvas_h=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)//2.3

	canvas=Canvas(window,width=canvas_w,height=canvas_h)
	canvas.pack()
	canvas.bind("<Button-1>",draw_line)	
def update_frame():
	global canvas,photo,window
	ret,frame=cap.read()
	frame=cv2.resize(frame,dsize=None,fx=0.5,fy=0.5)
	frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.create_image(0,0,image=photo,anchor=tkinter.NW)
	window.after(60,update_frame)
	now = datetime.datetime.now()
	name=Label(canvas,text="%d:%d:%d %d-%d-%d"%(now.day, now.month,now.year,now.hour,now.minute,now.second))
	name.place(x=20,y=20)

click_number=0	
def draw_line(event):
	global click_number
	global x1,y1
	global x2,y2
	global points,canvas,frame
	
	if click_number==0:
		x1=event.x
		y1=event.y
		
		points.append((x1,y1))
		print(points)
		click_number=1
             
	else:
		x2=event.x	
		y2=event.y
		canvas.create_line(x1,y1,x2,y2,fill="black",width=10)
		points.append((x2,y2))
		click_number=0

bt3=Button(window,text="chọn file",command=layfile)
bt3.place(x=350,y=550,width=100,height=40)
bt=Button(window,text="BẮT ĐẦU",command=update_frame)
bt.place(x=300,y=500,width=200,height=40)


def amthanh():
	winsound.PlaySound('E:/tin/tin hoc tre/2023/Intrusion_Warning-main/yolov8-live-master/canhbao.wav',winsound.SND_FILENAME)


def send_sms_cap():
  	try:
  		my_token = "6189869386:AAHIb6rcUzj43T3NQeo0_znrq2RbbMdUuzQ"
  		bot = telegram.Bot(token=my_token)
  		bot.sendPhoto(chat_id="6231784055", photo=open("alert.png", "rb"), caption="Có xâm nhập, nguy hiêm!")
  	except Exception as ex:
  		print("Can not send message telegram ", ex)

  	print("Send sucess")
  	client=Client("ACf37a9df101183714d968486cf420c524","1f0781ccb50697e41d99bb16cfad8a57")
  	message=client.messages.create(
  		body="canh bao co nguoi lay do",
  		from_ ="+13158175369",
  		to="+84363839173"
  		)

box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
def isInside(points, centroid):
	
    pl = Polygon(points)
    centroid = Point(centroid)
    print(pl.contains(centroid))
    return pl.contains(centroid)
seconds=time.time()   
seconds1=time.time()
goc=seconds1
tggoc=time.time()
def inside(points,centroid):

    global seconds,canvas,seconds1
    if isInside(points, centroid)==False:
    	seconds1+=1
    	if (seconds1-tggoc)>5 and isInside(points,centroid)==False:
	        cv2.imwrite("alert.png", cv2.resize(frame, dsize=None, fx=0.8, fy=0.8))
	        if int(seconds-tggoc)%15==0 :
	            al=Label(canvas,text="ALARM!!!",font=("Times New Roman",17))
	            al.place(x=20,y=200)	
	            
	            thread1=Thread(target=send_sms_cap)  
	            thread1.start()
	            thread2=Thread(target=amthanh)
	            thread2.start()
        	seconds+=1     	
seconds2=time.time()        		     
def inside1(points,centroid):

    global seconds,canvas,seconds2
    if isInside(points, centroid)==True:
    	seconds2+=1
    	if (seconds2-tggoc)>3 and isInside(points,centroid)==True:
	        cv2.imwrite("alert.png", cv2.resize(frame, dsize=None, fx=0.8, fy=0.8))
	        if int(seconds-tggoc)%7==0 :
	            al=Label(canvas,text="ALARM!!!",font=("Times New Roman",17))
	            al.place(x=20,y=50)	
	            
	            thread1=Thread(target=send_sms_cap)  
	            thread1.start()
	            thread2=Thread(target=amthanh)
	            thread2.start()
        	seconds+=1     	    
detect=True
i=0
def threadbutton1():
	b1=Thread(target=detectngay)
	b1.start()
def threadbutton2():
	b2=Thread(target=detectdem)
	b2.start()	
def detectngay():
	global detect,tggoc,seconds,frame,centroid,i
	while True:

		ret,frame=cap.read()
		frame=cv2.resize(frame,dsize=None,fx=0.5,fy=0.5)
		i=i+1
		if i%1==0:
		
			results=model(frame,agnostic_nms=True)[0]
			centroid=(0,0)
			for result in results:
				for r in result.boxes.data.tolist():
					x1,x2,y1,y2,score,class_id = r
					x1=int(x1)
					x2=int(x2)
					y2=int(y2)
					y1=int(y1)    
					print(class_id)

				if int(class_id)==1 or int(class_id)==2  or int(class_id)==24 or int(class_id)==26 or int(class_id)==39 or int(class_id)==62 or int(class_id)==67 or int(class_id)==63:
					centroid=((x1+x2)//2,(y1+y2)//2)
					cv2.circle(frame, centroid ,5,(255,0,0),-1)
					print(centroid)
			detections=sv.Detections.from_yolov8(results)
			labels=[
					f"{model.model.names[class_id]} {confidence:0.2f}"
					for _,confidence,class_id,_
					in detections
			]	
			inside(points,centroid)
		
def detectdem():
	global detect,tggoc,seconds,frame,centroid,i
	while True:
		ret,frame=cap.read()
		frame=cv2.resize(frame,dsize=None,fx=0.5,fy=0.5)
		i=i+1
		if i%1==0:
		
			results=model(frame,agnostic_nms=True)[0]
			centroid=(0,0)
			for result in results:
				for r in result.boxes.data.tolist():
					x1,x2,y1,y2,score,class_id = r
					x1=int(x1)
					x2=int(x2)
					y2=int(y2)
					y1=int(y1)    
					print(class_id)

				if int(class_id)==0:
					centroid=((x1+x2)//2,(y1+y2)//2)
					cv2.circle(frame, centroid ,5,(255,0,0),-1)
					print(centroid)
			detections=sv.Detections.from_yolov8(results)
			labels=[
					f"{model.model.names[class_id]} {confidence:0.2f}"
					for _,confidence,class_id,_
					in detections
			]	
			inside1(points,centroid)
bt1=Button(window,text="Camera Ngay",command=threadbutton1)
bt1.place(x=600,y=500,width=100,height=40)
bt2=Button(window,text="Camera Dem",command=threadbutton2)
bt2.place(x=100,y=500,width=100,height=40)




window.mainloop()

