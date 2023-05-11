import face_recognition
import cv2
import pickle
import os
import firebase_admin
from firebase_admin import db, storage
from firebase_admin import credentials

cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://faceattendance-system-default-rtdb.firebaseio.com/",
    'storageBucket' : "faceattendance-system.appspot.com"
})

folderStudents = 'Resources/Class'
encodelist = []
studentslist = os.listdir(folderStudents)

studentsimgs, studentsIds = zip(*[(cv2.imread(os.path.join(folderStudents, path)), os.path.splitext(path)[0]) for path in studentslist])
bucket = storage.bucket()
[storage.bucket().blob(f'Class/{path}').upload_from_filename(f'{folderStudents}/{path}') for path in studentslist]
print(len(studentsimgs))
print(studentsIds)

def findEncoding(student):
    global encodelist
    for img in student:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

print("Encodeing Starting.........")
knownEncodingList = findEncoding(studentsimgs)
knownEncodingListWithId = [knownEncodingList, studentsIds]
print("Encoding Ended.......")

with open("Encodes.p", "wb") as file:
    pickle.dump(knownEncodingListWithId, file)
