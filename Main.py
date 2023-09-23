import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import Tracker
import time
import math

model = YOLO('yolov8n.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('2.mp4')
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_rate = int(cap.get(5))

# Define the codec and create a VideoWriter object for MP4
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi', fourcc, 25, (frame_width, frame_height))

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 0

tracker = Tracker()

cy1 = 190
cy2 = 250

offset = 6

vh_down = {}
counter = []

vh_up = {}
counter1 = []

# Dictionary to store car speeds
car_speeds = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 3 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    a = results[0].boxes.boxes
    px = pd.DataFrame(a).astype("float")
    car_list = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' or 'truck' in c:
            car_list.append([x1, y1, x2, y2])  # Remove class ID as it's not needed

    bbox_id = tracker.update(car_list)

    for bbox_id_item in bbox_id:
        x3, y3, x4, y4, id = bbox_id_item  # The tracker returns [x, y, w, h, id]
        cx = (x3 + x4) // 2
        cy = (y3 + y4) // 2

         #going Up
        if cy1<(cy+offset) and cy1 > (cy-offset):
            vh_down[id]=cy
        if id in vh_down:
            if cy2<(cy+offset) and cy2 > (cy-offset):

                cv2.circle(frame,(cx,cy),1,(0,0,255),-3)
                cv2.putText(frame, f'Car {id}', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
                if counter.count(id)==0:
                    counter.append(id)

        #going Down
        if cy2<(cy+offset) and cy2 > (cy-offset):
            vh_up[id]=cy
        if id in vh_up:
            if cy1<(cy+offset) and cy1 > (cy-offset):
                cv2.circle(frame,(cx,cy),1,(0,0,255),-3)
                cv2.putText(frame, f'Car {id}', (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.1, (0, 255, 0), 1, cv2.LINE_AA)
                if counter1.count(id)==0:
                   counter1.append(id)

        if cy1 < (cy + offset) and cy1 > (cy - offset):
            vh_down[id] = time.time()
        if id in vh_down:
            if cy2 < (cy + offset) and cy2 > (cy - offset):
                elapsed_time = time.time() - vh_down[id]
                if id not in car_speeds:
                    car_speeds[id] = 0  # Initialize the speed for this car
                if elapsed_time > 0:
                    distance = 40  # meters
                    a_speed_ms = distance / elapsed_time
                    car_speeds[id] = a_speed_ms * 3.6  # Update the car's speed

        if cy2 < (cy + offset) and cy2 > (cy - offset):
            vh_up[id] = time.time()
        if id in vh_up:
            if cy1 < (cy + offset) and cy1 > (cy - offset):
                elapsed1_time = time.time() - vh_up[id]
                if id not in car_speeds:
                    car_speeds[id] = 0  # Initialize the speed for this car
                if elapsed1_time > 0:
                    distance1 = 40  # meters
                    a_speed_ms1 = distance1 / elapsed1_time
                    car_speeds[id] = a_speed_ms1 * 3.6  # Update the car's speed

        # Update the position of the speed text for this car
        speed_text_x = x3
        speed_text_y = y3 - 10  # Place it just above the car's bounding box
        
        # Check if the car id exists in car_speeds dictionary before accessing it
        if id in car_speeds:
            # Draw bounding box for the car
            cv2.rectangle(frame, (x3, y3), (x4, y4), (255, 0, 0), 1)

            # Draw the speed text at the updated position
            car_speed_text = f'{int(car_speeds[id])} '
            (car_speed_text_width, _), _ = cv2.getTextSize(car_speed_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            cv2.putText(frame, car_speed_text, (speed_text_x, speed_text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

            # Calculate the position for the "km/h" text
            kmh_text = 'km/h'
            kmh_text_width, _ = cv2.getTextSize(kmh_text, cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 0.8, 1)
            kmh_text_x = speed_text_x + car_speed_text_width  # Position it next to the car speed text
            kmh_text_y = speed_text_y 
            cv2.putText(frame, kmh_text, (kmh_text_x, kmh_text_y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255,0), 1, cv2.LINE_AA)

    cv2.line(frame, (180, cy1), (775, cy1), (255, 255, 255), 1)
    #cv2.putText(frame, 'Lane 1', (277, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA)

    cv2.line(frame, (21,cy2), (900, cy2), (255, 255, 255), 1)
    #cv2.putText(frame, 'Lane 2', (182, 367), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA)

    d = len(counter)
    u = len(counter1)
    cv2.putText(frame, f'Entering {u}', (775, 90), cv2.FONT_HERSHEY_TRIPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
    cv2.putText(frame, f'Leaving: {d}', (60, 90), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    frame = cv2.resize(frame, (frame_width, frame_height), cv2.INTER_LANCZOS4)

    out.write(frame)
    frame2 = cv2.resize(frame, (1020, 500))
    cv2.imshow("RGB", frame2)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
