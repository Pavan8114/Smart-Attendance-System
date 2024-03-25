import cv2
import face_recognition
import os
import csv
import datetime
import numpy as np

# Load the training images and their labels
path = 'C:\Users\pavan\OneDrive\Desktop\face-recognition-staff-attendance-main\images'
images = []
classNames = []
mylist = os.listdir(path)
for cl in mylist:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# Encode the training images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded_face = face_recognition.face_encodings(img)[0]
        encodeList.append(encoded_face)
    return encodeList

encoded_face_train = findEncodings(images)

# Initialize the CSV file for attendance
with open('Attendance.csv','w+') as f:
    myDataList = f.readlines()
    if len(myDataList)==0:
        now = datetime.datetime.now()
        date = now.strftime('%d-%B-%Y')
        time = now.strftime('%I:%M:%S:%p')
        f.writelines(f'Name,Date,Time\n')
        f.writelines(f'{classNames[0]},{date},{time}\n')

# Capture video from the webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    faces_in_frame = face_recognition.face_locations(imgS)
    encoded_faces = face_recognition.face_encodings(imgS, faces_in_frame)

    # Compare faces with the training images
    for encode_face, faceloc in zip(encoded_faces,faces_in_frame):
        matches = face_recognition.compare_faces(encoded_face_train, encode_face)
        faceDist = face_recognition.face_distance(encoded_face_train, encode_face)
        matchIndex = np.argmin(faceDist)

        # If a match is found, mark attendance and display the name
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            with open('Attendance.csv','r+') as f:
                myDataList = f.readlines()
                for line in myDataList:
                    if name in line:
                        continue
                    else:
                        now = datetime.datetime.now()
                        date = now.strftime('%d-%B-%Y')
                        time = now.strftime('%I:%M:%S:%p')
                        f.writelines(f'n{name}, {date}, {time}')
            cv2.rectangle(img, (faceloc[3], faceloc[0]),(faceloc[1], faceloc[2]), (0,255,0), 2)
            cv2.rectangle(img, (faceloc[1], faceloc[0]-35),(faceloc[1], faceloc[0]), (0,255,0), cv2.FILLED)
            cv2.putText(img,name, (faceloc[1]+6,faceloc[0]-5), cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)

        cv2.imshow('webcam', img)
        cv2.waitKey(1)