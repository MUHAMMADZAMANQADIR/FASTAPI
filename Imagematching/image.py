import cv2
import numpy as np
import face_recognition
import os

 
 
path = 'ImagesBasic'
images = []
classNames = []
myList = os.listdir(path)
inputpath=""
matchIndex=-1;
print(myList)
encodeList = []
matches=[]
#loading names


for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def name():
    global inputpath
    global matches
    from routes.test import getpath
    inputpath=getpath()
    
    matchpicture(inputpath)
    global matchIndex
    if matches[matchIndex]:
        name = classNames[matchIndex].upper()
         
        return name 
    else:
        print("Not FOUND")
        return name

def findEncodings(images):
     
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print(len((encodeListKnown)))
print('Encoding Complete')


def matchpicture(inputpath):
    global matches
    global matchIndex
    #cap = cv2.VideoCapture(0)
    #success, img = cap.read()
    img=face_recognition.load_image_file(inputpath)
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

        matchIndex = np.argmin(faceDis)
     



 

 


