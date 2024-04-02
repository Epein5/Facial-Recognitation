
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from backend import data

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-recog-196bc-default-rtdb.firebaseio.com/"
})

ref = db.reference('Student')


for key, value in data.data.items():
    ref.child(key).set(value)