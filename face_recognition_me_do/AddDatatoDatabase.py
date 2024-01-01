import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendancerealtime-87fde-default-rtdb.firebaseio.com/'
})

ref = db.reference('Student')

data = {
    "B21DCCN002":
        {
            "firstname": "Murtaza",
            "lastname" : "Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "email": "hassan@stu.ptit.edu.vn",
            "class": "D21CQCN05-B",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "B21DCCN003":
        {
            "firstname": "Emly",
            "lastname" : "Plon",
            "major": "Economics",
            "starting_year": 2021,
            "class": "D21DCCN05-B",
            "email": "emly@stu.ptit.edu.vn",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "B21DCCN004":
        {
            "firstname": "Elon Musk",
            "lastname": "Musk",
            "major": "Physics",
            "starting_year": 2020,
            "class": "D21DCCN05-B",
            "email": "elon@stu.ptit.edu.vn",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "B21DCCN281":
        {
            "firstname": "Le Dinh" ,
            "lastname": "Duong",
            "major": "CNTT",
            "starting_year": 2021,
            "class": "D21DCCN05-B",
            "email": "duongld@stu.ptit.edu.vn",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "B21DCCN001":
        {
            "firstname": "Le Thi Mai",
            "lastname" : "Linh",
            "major": "Doctor",
            "starting_year": 2021,
            "class": "D21DCCN05-B",
            "email": "linhltm@stu.ptit.edu.vn",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "B21DCCN233":
        {
            "firstname": "Duong Van" ,
            "lastname" :"Du",
            "major": "CNTT",
            "starting_year": 2021,
            "class": "D21DCCN05-B",
            "email": "dudv@stu.ptit.edu.vn",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "B21DCCN569":
        {
            "firstname": "Trinh Tan ",
            "lastname": "Nguyen",
            "major": "CNTT",
            "starting_year": 2021,
            "class": "D21DCCN05-B",
            "email": "nguyentt@stu.ptit.edu.vn",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key,value in data.items():
    ref.child(key).set(value)