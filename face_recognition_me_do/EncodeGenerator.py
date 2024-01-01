import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-87fde-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-87fde.appspot.com"
})

# Từ đường dẫn của sinh viên đưa vào list các ảnh
folderPath = "Images"
pathList = os.listdir(folderPath)
imgList = []
studentsId = []

# print(modePathList)
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path))) #  duyệt theo lấy dđườg dẫn của từng ảnh
    studentsId.append(os.path.splitext(path)[0]) # Lấy id là phần trước của đường dẫn bằng cách dùng hàm splitex

    #  thêm dữ liệu vào database
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
print(studentsId)


def findEncodeings(imagesList): # hàm mã hóa ảnh và trẻ về list các mã  hóa
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

encodeListKnown = findEncodeings(imgList) #gọi hàm mã hóa để mã hóa các ảnh trong imagesList
encodeListKnownWithIds = [encodeListKnown,studentsId]

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()