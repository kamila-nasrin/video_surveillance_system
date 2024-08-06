from time import strftime

import cv2
import datetime
import numpy as np
# from SJV.DBConnection import *
import pymysql
from django.db import connection
from videosurveillance_app.cnnpredict import predict
import matplotlib.pyplot as plt
# from fapp.models import notification_table
import requests
import os
import pygame
labelsPath = os.path.sep.join(["yolo-coco", "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# classes = ["Sign Board"]
# with open("coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]


np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")


weightsPath = os.path.sep.join(["yolo-coco", "yolov3.weights"])
configPath = os.path.sep.join(["yolo-coco", "yolov3.cfg"])

net1 = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net1.getLayerNames()
ln = [ln[i[0] - 1] for i in net1.getUnconnectedOutLayers()]


live_Camera = cv2.VideoCapture(1)
lower_bound = np.array([11, 33, 111])

upper_bound = np.array([90, 255, 255])

# Initialize pygame
pygame.mixer.init()
alert_sound=pygame.mixer.Sound('alarm.mp3')


def main_code():
    (W, H) = (None, None)
    while (live_Camera.isOpened()):

        ret, frame = live_Camera.read()

        if W is None or H is None:
            (H, W) = frame.shape[:2]

        frame = cv2.resize(frame, (1280, 720))

        frame = cv2.flip(frame, 1)

        frame_smooth = cv2.GaussianBlur(frame, (7, 7), 0)

        mask = np.zeros_like(frame)

        mask[0:720, 0:1280] = [255, 255, 255]

        img_roi = cv2.bitwise_and(frame_smooth, mask)

        frame_hsv = cv2.cvtColor(img_roi, cv2.COLOR_BGR2HSV)
        image_binary = cv2.inRange(frame_hsv, lower_bound, upper_bound)
        check_if_fire_detected = cv2.countNonZero(image_binary)
        print("check",check_if_fire_detected)
        v=4
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net1.setInput(blob)
        #
        layerOutputs = net1.forward(ln)

        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []
        pl = []
        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > 0.5:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.4,
                                0.5)
        pcount = 0
        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                # draw a bounding box rectangle and label on the frame
                color = [int(c) for c in COLORS[classIDs[i]]]

                text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                           confidences[i])
                if LABELS[classIDs[i]] == "person":
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    pl.append("1")
                    pcount += 1
                    cropped_image = frame[y:y + h, x:x + w]

                    # res = predict("sample.png")
                    # print(res,"===========")

                    # cv2.putText(frame, "person", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, print_color, 2)
        if len(pl)==0:
         if int(check_if_fire_detected) >= 5000:
            # cv2.putText(frame, "Fire Detected !", (300, 60), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 2)
            # fn = 'sample.jpg'
            fn = strftime("%Y%m%d%H%M%S") + ".png"
            fn1=r"C:\Users\Kareem\PycharmProjects\videosurveillance\media/" + fn
            cv2.imwrite(r"C:\Users\Kareem\PycharmProjects\videosurveillance\media/" + fn, frame)
            # cv2.imwrite(fn,frame)
            res1=predict(fn1)
            print(res1[0],"====================")
            if res1[0]==1:
                alert_sound.play()
                # print("******************************************************************************************")
                # print("******************************************************************************************")
                # print("******************************************************************************************")
                # print("******************************************************************************************")
                # print("******************************************************************************************")
                # print("******************************************************************************************")
                # requests.get("http://127.0.0.1:8000/notification_insert/4/"+fn)


                # cursor= connection.cursor()
                con=pymysql.connect(host='localhost',port=3308,user='root',password='12345678',db='videosurveillance')
                cmd=con.cursor()
                cmd.execute("SELECT MINUTE (TIMEDIFF(CURTIME(), `time`)) AS minu FROM `videosurveillance_app_alerttable` WHERE `camera_id`=1 ORDER BY id DESC LIMIT 1")
                cmd.fetchone()

                cmd.execute("SELECT MINUTE (TIMEDIFF(CURTIME(), `time`)) AS minu FROM `videosurveillance_app_alerttable` WHERE `camera_id`='"+str(v)+"' ORDER BY id DESC LIMIT 1")
                res=cmd.fetchone()
                print(res,"000000000000000000000000")
                print("detected")
                if res is None:
                    # q = "insert into notify values(null,%s,' Forest Fire detected ,Please Take Further Action ',curdate(),curtime(),'detected') "
                    # iud(q, v)
                    # ob=notification_table()
                    # ob.date=datetime.now()
                    # ob.time=datetime.now()
                    # ob.image=fn
                    # ob.type='fire'
                    # ob.save()
                    cmd.execute("INSERT INTO `videosurveillance_app_alerttable` VALUES(NULL,'fire','pending',CURDATE(),CURTIME(),'"+fn+"',1)")
                    con.commit()
                else:
                    mi=res[0]
                    print("minute",mi)
                    if mi>=1:

                        cmd.execute("select * from videosurveillance_app_alerttable where camera_id=1 and date=curdate() and time=curtime()")

                        # cmd.execute(q)

                        res=cmd.fetchone()
                        if res is None:
                            cmd.execute(
                                "INSERT INTO `videosurveillance_app_alerttable` VALUES(NULL,'fire',CURDATE()',CURTIME(),'" + fn + "),4")
                            con.commit()
                              # ob=notification_table()
                              # ob.date=datetime.now()
                              # ob.time=datetime.now()
                              # ob.photo=fn
                              # ob.type='fire'
                              # ob.save()

        cv2.imshow("Fire Detection", frame)

        if cv2.waitKey(10) == 27:
            print("break")
            break
    live_Camera.release()

    cv2.destroyAllWindows()
main_code()