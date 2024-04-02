import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
import json
from data import data
# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://face-recog-196bc-default-rtdb.firebaseio.com/",
#     'storageBucket': "face-recog-196bc.appspot.com"
# })
def encodegenerator():
    # Importing student images
    folderPath = '../Images/'
    pathList = os.listdir(folderPath)
    print(pathList)
    imgList = []
    studentIds = []
    for path in pathList:
        imgList.append(cv2.imread(os.path.join(folderPath, path)))
        studentIds.append(os.path.splitext(path)[0])

        fileName = f'{folderPath}/{path}'
        bucket = storage.bucket()
        blob = bucket.blob(fileName)
        blob.upload_from_filename(fileName)

    print(studentIds)


    def findEncodings(imagesList):
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)

        return encodeList


    print("Encoding Started ...")
    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    print("Encoding Complete")

    file = open("../EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print("File Saved")

    return encodeListKnownWithIds



def adddatatodatabase():
    # cred = credentials.Certificate("../serviceAccountKey.json")
    # firebase_admin.initialize_app(cred, {
    #     'databaseURL': "https://face-recog-196bc-default-rtdb.firebaseio.com/",
    # })
    ref = db.reference('Student')
    for key, value in data.items():
        ref.child(key).set(value)
    return "Data added to database"

# def add_item(new_data):
#     with open('data.py', 'r') as f:
#         lines = f.readlines()

#     if lines:
#         lines.pop()

#     # Write the modified lines back to the file
#     with open('data.py', 'w') as f:
#         f.writelines(lines)
    
#     with open('data.py', 'a') as f:
#         f.write(',')
#         a = json.dumps(new_data, indent=4)
#         f.write(a[1:])