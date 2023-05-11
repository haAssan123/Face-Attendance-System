import cv2
import cvzone
import face_recognition
import os
import numpy as np
import pickle
from datetime import datetime
from datetime import timedelta, time
import firebase_admin
from firebase_admin import db, storage
from firebase_admin import credentials

cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://faceattendance-system-default-rtdb.firebaseio.com/",
    'storageBucket' : "faceattendance-system.appspot.com"
})
bucket = storage.bucket()
blob = bucket.blob('Class')

cap = cv2.VideoCapture(0)
def imgReszing(img):
    img_small =cv2.resize(img, (216,216))
    cv2.imshow("orignal", img)
    cv2.imshow("small img", img_small)

imgBackground = cv2.imread('Resources/Attendance Resources/background.png')
folderMode = 'Resources/Attendance Resources/Modes'
modelist = os.listdir(folderMode)
mode = [cv2.imread(os.path.join(folderMode, path)) for path in modelist]

with open("Encodes.p", "rb") as file:
    knownEncodingListWithId = pickle.load(file)
knownEncodingList, studentsIds = knownEncodingListWithId

modeType = 0
frame_counter = 0


while True:

    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    currentFrame = face_recognition.face_locations(imgS)
    encodeFrameFace = face_recognition.face_encodings(imgS, currentFrame)
    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = mode[modeType]

    if currentFrame:
        for encode, faceLoc in zip(encodeFrameFace, currentFrame):
            matches = face_recognition.compare_faces(knownEncodingList, encode)
            faceDis = face_recognition.face_distance(knownEncodingList, encode)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentsIds[matchIndex]
                if frame_counter == 0:
                    frame_counter = 1
                    modeType = 1

        if frame_counter!=0:
            if frame_counter == 1:
                studentsInfo = db.reference(f"Candidates/{id}").get()
                blob = bucket.get_blob(f"Class/{id}.png")
                arr = np.frombuffer(blob.download_as_string(), np.uint8)
                studentIdentificationImg = cv2.imdecode(arr, cv2.COLOR_BGRA2BGR)
                datetime_obj = datetime.strptime(studentsInfo["last_attendance_time"], "%Y-%m-%d %H:%M:%S")
                secs = (datetime.now()-datetime_obj).total_seconds()
                if secs > 30:
                    refrence_ = db.reference(f"Candidates/{id}")
                    studentsInfo['total_attendance']+=1
                    refrence_.child('total_attendance').set(studentsInfo['total_attendance'])
                    refrence_.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    print(studentsInfo)
                else:
                    modeType=3
                    frame_counter=0
                    imgBackground[44:44 + 633, 808:808 + 414] = mode[modeType]

            if 10<frame_counter<20:
                modeType = 2

            if modeType != 3:
                if frame_counter <=10:
                    cv2.putText(imgBackground, str(studentsInfo['total_attendance']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentsInfo['major']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(id), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentsInfo['standing']), (910, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentsInfo['year']), (1025, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    cv2.putText(imgBackground, str(studentsInfo['starting_year']), (1125, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                    (w, h), _ = cv2.getTextSize(studentsInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentsInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                    imgBackground[175:175+216, 909:909+216] = studentIdentificationImg

                frame_counter+=1

                if frame_counter >= 20:
                    modeType =0
                    frame_counter =0
                    studentsInfo =0
                    imgBackground[44:44 + 633, 808:808 + 414] = mode[modeType]

    else:
        modeType = 0
        frame_counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('m'):
        break