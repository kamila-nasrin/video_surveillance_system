import datetime

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
from pygame import mixer

from videosurveillance_app.predict import predict_burglary

mixer.init()
import os
from videosurveillance_app.DBConnection import Db
from videosurveillance_app.classify import classify
police_id=1
# image_path=r"A:\KIRAN_COLLEGE\MAJOR PROJECT\main project\robbery\robbery\home\images\\"

def detect_and_predict_mask(frame, faceNet, maskNet):

	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]


		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		print(confidence,"confidence")
		print(confidence,"confidence")
		print(confidence,"confidence")
		print(confidence,"confidence")
		print(confidence,"confidence")
		if confidence > 0.2:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			try:
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# ensure the bounding boxes fall within the dimensions of
				# the frame
				(startX, startY) = (max(0, startX), max(0, startY))
				(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

				# extract the face ROI, convert it from BGR to RGB channel
				# ordering, resize it to 224x224, and preprocess it
				face = frame[startY:endY, startX:endX]
				face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
				face = cv2.resize(face, (224, 224))
				face = img_to_array(face)
				face = preprocess_input(face)
				face = np.expand_dims(face, axis=0)

				# add the face and bounding boxes to their respective
				# lists
				# add the face and bounding boxes to their respective
				# lists
				if len(faces) == 0:
					faces = face
				else:
					faces = np.concatenate((faces, face), axis=0)
				locs.append((startX, startY, endX, endY))

			except:
				pass

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		preds = maskNet.predict(faces)
		print("#################################")
		print(len(preds),preds)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="face_detector",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\face_detector\deploy.prototxt", r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\face_detector\res10_300x300_ssd_iter_140000.caffemodel")

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(r'C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\mask_detector.model')

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
time.sleep(2.0)
burglary_cnt=0
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400)

	# detect faces in the frame and determine if they are wearing ae
	# face mask or not
	(locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

	# loop over the detected face locations and their corresponding
	# locations
	print((locs, preds))
	for (box, pred) in zip(locs, preds):
		# unpack the bounding box and predictions
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred
		print(mask,"jjjjjjjjjjjjjjjjjjjjjjjjjjjj")
		print(mask,"jjjjjjjjjjjjjjjjjjjjjjjjjjjj")
		print(mask,"jjjjjjjjjjjjjjjjjjjjjjjjjjjj")
		print(mask,"jjjjjjjjjjjjjjjjjjjjjjjjjjjj")
		if mask>.7:
			print("Mask detected===========")
			print("Mask detected===========")
			print("Mask detected===========")
			cv2.imwrite(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\sample.jpg", img=frame)
			pred, score=classify(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\sample.jpg")
			print( score,"================")
			print( score,"================")
			print( score,"================")
			print( score,"================")


			if score > 0.3:
				print("With mask detected and weapon ", score * 100)
				mixer.music.load(r'C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\alarm.mp3')
				mixer.music.play()
				d=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
				cv2.imwrite(r"C:\Users\Kareem\PycharmProjects\videosurveillance\media/" + d +".jpg", frame)
				path=r"C:\Users\Kareem\PycharmProjects\videosurveillance\media/" + d + ".jpg"
				db=Db()
				db.insert("INSERT INTO `videosurveillance_app_alerttable` VALUES(NULL,'theif','pending',CURDATE(),CURTIME(),'"+d + ".jpg"+"',1)")

		pred=predict_burglary(r"C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\sample.jpg")
		print(pred,"pred")
		print(pred,"pred")
		print(pred,"pred")
		print(pred,"pred")
		print(pred,"pred")
		####BEHAVIOUR
		if pred[0] == 1:
			print("burglary ",
				  burglary_cnt)
			burglary_cnt+=1
			if burglary_cnt==5:

				mixer.music.load(r'C:\Users\Kareem\PycharmProjects\videosurveillance\videosurveillance_app\alarm.mp3')
				mixer.music.play()
				print("Burglary detected")
				d = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
				cv2.imwrite(r"C:\Users\Kareem\PycharmProjects\videosurveillance\static\detections\\" + d + ".jpg", frame)
				path = "/static/detections/" + d + ".jpg"
				# db = Db()
				# db.insert("INSERT INTO `home_detection` VALUES(NULL, 'pending', NOW(), '" + str(
				# 	police_id) + "', '" + path + "')")
				burglary_cnt=0


		# determine the class label and color we'll use to draw
		# the bounding box and text
		label = "Mask" if mask > withoutMask else "No Mask"
		color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

		# include the probability in the label
		label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)


		# display the label and bounding box rectangle on the output
		# frame
		# cv2.putText(frame, label, (startX, startY - 10),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
		# cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
