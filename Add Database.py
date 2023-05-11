import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate("service.json")
firebase_admin.initialize_app(cred,{
    'databaseURL' : "https://faceattendance-system-default-rtdb.firebaseio.com/"
})

db_ref = db.reference("Candidates")

data = {

    "1233":
        {
            "name": "Muhammad Hassan",
            "major": "Senior Data Scientist",
            "starting_year": 2020,
            "total_attendance": 0,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1234":
        {
            "name": "Elon Musk",
            "major": "Automating Life",
            "starting_year": 2012,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1235":
        {
            "name": "Jeff Bezos",
            "major": "E-Commerce",
            "starting_year": 2000,
            "total_attendance": 0,
            "standing": "A",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1236":
        {
            "name": "Larry Page",
            "major": "Google Programmer",
            "starting_year": 2000,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1237":
        {
            "name": "Mark Zuckerberg",
            "major": "Facebook Programmer",
            "starting_year": 2008,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1238":
        {
            "name": "Sundar Pichai",
            "major": "Marketing",
            "starting_year": 2017,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1239":
        {
            "name": "Warren Buffett",
            "major": "Investor",
            "starting_year": 2009,
            "total_attendance": 0,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },

}


for key, value in data.items():
    db_ref.child(key).set(value)
