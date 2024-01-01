import csv              #Đọc các file excel định dạng .csv
import os               #Làm việc với các tậ ptin và thư mục
import pickle           #Lưu trữ dữ liệu dưới dạng Byte
import cv2              #Sử dụng Camera
import face_recognition #Nhận diện& xử lý khuôn mặt
import numpy  as np     #tính toán phức tạp
import cvzone           #Hiện khung viền xung quanh khuôn mặt nhận diện
import firebase_admin   #lưu trữ và bảo mật dữ liệu
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime #thư viện thời gian tính đến mili-giây

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendancerealtime-87fde-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-87fde.appspot.com"
})

bucket = storage.bucket()

cap =  cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread("Resources/background.png", )

# Từ đường dẫn của ảnh chức năng đưa vào list các ảnh
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
# print(modePathList)
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path))) #  duyệt theo lấy dđườg dẫn của từng ảnh
# print(len(imgModeList))

#Load the encoding file
file = open('EncodeFile.p','rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown,studentsId = encodeListKnownWithIds
print(studentsId)

counter = 0
modeType = 0
id = -1
imgStudent = []

listDiscover = []

currentDate = datetime.now().strftime("%Y-%m-%d")
file_csv = open(f'{currentDate}.csv','w+', newline= '')
writeFile = csv.writer(file_csv)
writeFile.writerow(['Ma Sinh Vien','Ho','Ten'])

# hiển thị video trên nền
while True:
    print((listDiscover))
    success , img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS) # lấy v trí của khung hình hiện tại
    encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame) # mã hóa khung hình hiện tại

    imgBackground[162:162+480,55:55+640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        # so sánh curframe với các khung hình trong list
        for encodeFace , faceLoc in zip(encodeCurFrame,faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            print("matches" , matches)
            print("faceDis" , faceDis)
            matchIndex = np.argmin(faceDis)
            print(matchIndex)

            if matches[matchIndex]:
                print("phat hien")
                # print(studentsId[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                id = studentsId[matchIndex]
                print(id)

                if counter == 0 :
                    counter = 1
                    modeType = 1
        if id in listDiscover:
            modeType = 3
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
        else:
            if counter != 0:
                if counter == 1:
                    # Lấy dữ liệu của sinh viên từ database
                    studentInfo = db.reference(f'Student/{id}').get()
                    print(studentInfo)

                    # lấy ảnh từ database
                    blob = bucket.get_blob(f'Images/{id}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    #Update data  time
                    datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                       "%Y-%m-%d %H:%M:%S")
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)
                    # if secondsElapsed > 30:
                    #     ref = db.reference(f'Student/{id}')
                    #     studentInfo['total_attendance'] += 1
                    #     ref.child('total_attendance').set(studentInfo['total_attendance'])
                    #     ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    # else:
                    #     modeType = 3
                    #     counter = 0
                    #     imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:
                    if 10 < counter < 15 :
                        modeType = 2
                        if counter == 14 :
                            if id != -1 : listDiscover.append(id)
                            ref = db.reference(f'Student/{id}')
                            writeFile.writerow([id,ref.child('firstname').get(),ref.child('lastname').get()])


                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 10:
                        # hiển thị thông tin lên ảnh
                        cv2.putText(imgBackground, str(len(listDiscover)), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        # cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                        #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        (w, h), _ = cv2.getTextSize(studentInfo['firstname']+studentInfo['lastname'],
                                                    cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['firstname']+studentInfo['lastname']),
                                    (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                        imgBackground[175:175+216,909:909+216] = imgStudent

                counter+=1

                if counter >= 15:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    # if id != -1 : listDiscover.append(id)

    else:
        modeType = 0
        counter = 0


    # cv2.imshow("Web Cam",img)
    cv2.imshow("Face Attendance" , imgBackground)
    cv2.waitKey(1)

# file_csv.close()