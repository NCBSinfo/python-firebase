"""
Python script to update user database of NCBSinfo app
Database is hosted on Firebase Real Time Database

You will need following files (which are untracked from version control for security)
secrets/credentials.py # Contains all database urls, api keys and credentials
user_data/UserRegistration # Contains user registration data

Script uses pyrebase library : https://github.com/thisbejim/Pyrebase
"""

import pyrebase

from secrets.credentials import *

config = {
    "apiKey": API_KEY,
    "authDomain": AUTH_DOMAIN,  # ProjectID.firebaseapp.com
    "databaseURL": DATABASE_URL,
    "storageBucket": STORAGE_BUCKET,  # projectId.appspot.com
    "serviceAccount": "secrets/service_file.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# for i in range(5):
#     data = {
#         "name": "asdasdasd",
#         "id": 1
#     }
#     users = db.child("debug").child("user" + str(i)).update(data, user['idToken'])


all_users = db.child("authEmails").get()
for user in all_users.each():
    print(user.key())
    print(user.val())
