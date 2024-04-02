from fastapi import FastAPI, File, HTTPException, Request, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from firebase_admin import credentials, db, storage
import numpy as np
import time
import firebase_admin
import uvicorn
import base64
from fastapi.responses import JSONResponse
import subprocess
import json
import datetime
import cv2
from functions import encodegenerator, adddatatodatabase
from data import data

# Initialize Firebase
cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recog-196bc-default-rtdb.firebaseio.com/",
    'storageBucket': "face-recog-196bc.appspot.com"
})
bucket = storage.bucket()

IMAGEDIR =  "../Images/"
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    students_ref = db.reference('Student')
    students = students_ref.get()
    student_data = []

    for student_id, data in students.items():
        student_info = {
            'id': student_id,
            'name': data['name'],
            'major': data['major'],
            'year': data['year'],
            'total_attendance': data['total_attendance'],
            'attendance_times': data.get('attendance_times', [])  # Get attendance times or empty list if not available
        }
        # Fetch image from Firebase Storage and convert to base64
        blob = bucket.blob(f'Images/{student_id}.png')
        img_data = blob.download_as_string()
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        student_info['image'] = img_base64
        student_data.append(student_info)

    return templates.TemplateResponse("dashboard.html", {"request": request, "students": student_data})

@app.get("/attendance_times/{student_id}", response_class=HTMLResponse)
async def get_attendance_times(request: Request, student_id: str):
    student_ref = db.reference(f'Student/{student_id}')
    student_data = student_ref.get()
    if not student_data:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Retrieve student information
    student_name = student_data.get('name', '')
    student_major = student_data.get('major', '')
    student_year = student_data.get('year', '')
    
    # Retrieve attendance times
    attendance_times = student_data.get('attendance_times', [])
    
    # Fetch image from Firebase Storage and convert to base64
    blob = bucket.blob(f'Images/{student_id}.png')
    img_data = blob.download_as_string()
    student_image = base64.b64encode(img_data).decode('utf-8')

    return templates.TemplateResponse("attendance_times.html", 
                                      {"request": request, 
                                       "student_id": student_id, 
                                       "student_name": student_name, 
                                       "student_major": student_major,
                                       "student_year": student_year,
                                       "student_image": student_image,
                                       "attendance_times": attendance_times})

@app.get("/register", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("registration_form.html", {"request": request})


@app.post("/register_form")
async def register_student(request: Request, name: str = Form(...), major: str = Form(...), 
                           starting_year: int = Form(...), last_attendance_time: str = Form(...),
                            file: UploadFile = File(...)
                           ):
    contents = await file.read()
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    # Save form data to a JSON file
    a = file.filename[:-4]
    new_data = {
        a: {
            "name": name,
            "major": major,
            "starting_year": starting_year,
            "total_attendance": 0,
            "year": datetime.datetime.now().year - starting_year + 1,
            "REGISTERED_ON": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_attendance_time": last_attendance_time
        }
    }
    add_item(new_data)

    # encodegenerator()
    # adddatatodatabase(new_data)

    return {"message": "Please go to /last_page"}


@app.get("/last_page" ,response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("last_page.html", {"request": request})


@app.post("/run_python_files")
async def run_python_files():
    try:
        encodegenerator()
        adddatatodatabase()
        
        return {"message": "Please go back to Dashboard to see the changes"}
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


def add_item(new_data):
    with open('data.py', 'r') as f:
        lines = f.readlines()

    if lines:
        lines.pop()

    # Write the modified lines back to the file
    with open('data.py', 'w') as f:
        f.writelines(lines)
    
    with open('data.py', 'a') as f:
        f.write(',')
        a = json.dumps(new_data, indent=4)
        f.write(a[1:])