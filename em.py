import keras
import cv2
import time
from keras.models import model_from_json
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

import numpy as np
import numpy as np
import imutils
import requests

url = "http://192.0.0.4:8080/shot.jpg"





model = model_from_json(open(r"C:\Users\Kareem\PycharmProjects\videosurveillance\static\model\facial_expression_model_structure.json", "r").read())
model.load_weights(r'C:\Users\Kareem\PycharmProjects\videosurveillance\static\model\facial_expression_model_weights.h5')  # load weights


face_cascade = cv2.CascadeClassifier(r'C:\Users\Kareem\PycharmProjects\videosurveillance\static\model\haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(1)


emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')

def camclick():
    i=0
    while(True):
        ret, img = cap.read()
        # img_resp = requests.get(url)
        # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        # img = cv2.imdecode(img_arr, -1)
        # img = imutils.resize(img, width=1000, height=1800)
        # img = cv2.imread('../11.jpg')
        # cv2.imwrite(str(i)+".jpg",img)
        i=i+1

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        #print(faces) #locations of detected faces
        emotion=None
        if i % 5 == 0:
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) #draw rectangle to main image

                detected_face = img[int(y):int(y+h), int(x):int(x+w)] #crop detected face
                detected_face = cv2.cvtColor(detected_face, cv2.COLOR_BGR2GRAY) #transform to gray scale
                detected_face = cv2.resize(detected_face, (48, 48)) #resize to 48x48

                img_pixels = image.img_to_array(detected_face)
                img_pixels = np.expand_dims(img_pixels, axis = 0)

                img_pixels /= 255 #pixels are in scale of [0, 255]. normalize all pixels in scale of [0, 1]

                predictions = model.predict(img_pixels) #store probabilities of 7 expressions

                #find max indexed array 0: angry, 1:disgust, 2:fear, 3:happy, 4:sad, 5:surprise, 6:neutral
                max_index = np.argmax(predictions[0])

                emotion = emotions[max_index]
                # cv2.putText(img,emotion,(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
                print (emotion)

                req = time.strftime("%Y%m%d_%H%M%S") + ".jpg"
                cv2.imwrite(r"C:\Users\Kareem\PycharmProjects\videosurveillance\media\\"+req, img)
                qrr = requests.get("http://127.0.0.1:8000/insertEmotions/" + str(emotion) + "/" +str(1)+"/" +str(req))



                # if cv2.waitKey(1):
        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # press q to quit
            break

        # kill open cv things
    # cap.release()
    cv2.destroyAllWindows()
            # 	pass
        # return emotion
            #write emotion text above rectangle

camclick()