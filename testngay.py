import cv2
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
points = []
def send_sms_cap():
    try:
        my_token = "6189869386:AAHIb6rcUzj43T3NQeo0_znrq2RbbMdUuzQ"
        bot = telegram.Bot(token=my_token)
        bot.sendPhoto(chat_id="6231784055", photo=open("alert.png", "rb"), caption="Có xâm nhập, nguy hiêm!")
    except Exception as ex:
        print("Can not send message telegram ", ex)

    print("Send sucess")
    client=Client("ACec3b79a0ef4ad123c4ce577b9caf09d0","913586de0d0ae763a2c5ddbe19fc964b")
    message=client.messages.create(
        body="canh bao co nguoi lay do",
        from_ ="+12545874070",
        to="+84363839173"
        )
    
def isInside(points, centroid):
    pl = Polygon(points)
    centroid = Point(centroid)
    print(pl.contains(centroid))
    return pl.contains(centroid)
    
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame, (x, y), 3, (0, 0, 255), 3, cv2.FILLED)
        points.append((x, y))
        if len(points) >= 2:
            cv2.line(frame, points[-1], points[-2], (255, 0, 0), 5, cv2.LINE_AA)
        
    elif event == cv2.EVENT_RBUTTONDOWN:
        points.clear()

def draw_polygon(frame,points):
    if len(points) >= 2:
            cv2.line(frame, points[-1], points[-2], (255, 0, 0), 5, cv2.LINE_AA)
    return frame        
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--webcam-resolution", 
        default=[1280, 720], 
        nargs=2, 
        type=int
    )
    args = parser.parse_args()
    return args

tggoc=time.time()    
seconds = time.time()

def alarm():
    playsound("E:/tin/tin hoc tre/2023/Intrusion_Warning-main/yolov8-live-master/canhbao.mp3")
    
def inside(points,centroid):
    global seconds
    if isInside(points, centroid)==False:
        cv2.putText(frame, "ALARM!!!!", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)    
        if int(seconds-tggoc)%15==0:
            
            cv2.imwrite("alert.png", cv2.resize(frame, dsize=None, fx=0.2, fy=0.2))
            thread1=Thread(target=send_sms_cap)  
            thread1.start()
            thread2=Thread(target=alarm)
            thread2.start()
        seconds+=1  
        
        
    return isInside(points,centroid) 
    

args = parse_arguments()
frame_width, frame_height = args.webcam_resolution


cap = cv2.VideoCapture('E:/tin/tin hoc tre/2023/Intrusion_Warning-main/yolov8-live-master/ngày.mp4')

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

model = YOLO("yolov8n.pt")


box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )
detect=False


while True:
    now = datetime.datetime.now()
    ret, frame = cap.read()
    frame=imutils.resize(frame, width=700)
        
    results = model(frame, agnostic_nms=True)[0]
        
            
    for result in results:
        
            for r in result.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
            if int(class_id)==1:       
                centroid = ((x1 + x2) // 2, (y1 + y2) // 2)
                
                cv2.circle(frame, centroid, 5, (255,0,0), -1)

    cv2.putText(frame,"%d:%d:%d %d-%d-%d"%(now.day, now.month,now.year,now.hour,now.minute,now.second), (20, 70), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)  
    detections = sv.Detections.from_yolov8(results)
    
    labels = [
        f"{model.model.names[class_id]} {confidence:0.2f}"
        for _, confidence, class_id, _
        in detections         
        ]
        
    if int(class_id)==1:
        frame = box_annotator.annotate(
            scene=frame, 
            detections=detections, 
            labels=labels
            )
  
    frame=draw_polygon(frame,points)
            
    if detect==True:
        inside(points,centroid)    
       
    key = cv2.waitKey(1)
    if key == ord('q'):
            break
    elif key == ord('d'):
            points.append(points[0])
            detect=True
    elif key == ord('f'):
        detect=False        
    cv2.imshow("yolov8", frame)
    cv2.setMouseCallback('yolov8', click_event,points)        

