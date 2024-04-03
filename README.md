# Face Attendance System

This is a Face Attendance System implemented using Python, OpenCV, face_recognition library, and Firebase. It allows users to register students, track attendance, and view attendance records.

## Features

- Register new students with their information and images.
- Capture attendance using face recognition technology.
- View attendance records for each student.

## Setup

1. **Clone the Repository:**
   - Clone the repository to your local machine using the following command:
     ```
     git clone <repository-url>
     ```

2. **Set up Firebase:**
   - Create a Firebase project and download the service account key JSON file (`serviceAccountKey.json`).
   - Save the `serviceAccountKey.json` file in the main directory of the project.

3. **Create Image Directory:**
   - Create an empty directory named `Image` in the root directory of the project. This directory will be used to store student images.

4. **Download Resources:**
   - Download the resources required for the project from the link provided: [Face Recognition with Real-Time Database Resources](https://www.computervision.zone/courses/face-recognition-with-real-time-database/).
   - Keep the downloaded resources in your project's root directory.

5. **Install Dependencies:**
   - Install the required Python dependencies using the following command:
     ```
     pip install -r requirements.txt
     ```

6. **Start FastAPI Server:**
   - Start the FastAPI server using the following command:
     ```
     uvicorn main:app --reload
     ```

7. **Setup Data File:**
   - Before registering any users, ensure the `data.py` file located inside the `backend` directory is cleared. Remove any existing data and keep the file empty.
   - Your first registration may show an error due to the empty `data.py` file. Remove the trailing comma after the empty dictionary `{}` to resolve the error.

8. **Run the Face Recognition App:**
   - Run the `main.py` script to start the facial recognition application.
   - Use the FastAPI server for user registration and to access the admin dashboard.



## Usage

- Register new students by uploading their information and images.
- Run the attendance system to mark attendance using face recognition.
- View attendance records through the web dashboard.

## Feel Free to Fork and Contribute. 
