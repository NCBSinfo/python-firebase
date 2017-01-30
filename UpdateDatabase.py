"""
Python script to update user database of NCBSinfo app
Database is hosted on Firebase Real Time Database

You will need following files (which are untracked from version control for security)
secrets/credentials.py # Contains all database urls, api keys and credentials
user_data/UserRegistration # Contains user registration data
"""

import pyrebase

from secrets.credentials import *

config = {
    "apiKey": API_KEY,
    "authDomain": AUTH_DOMAIN,  # ProjectID.firebaseapp.com
    "databaseURL": DATABASE_URL,
    "storageBucket": STORAGE_BUCKET,  # projectId.appspot.com
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(EMAIL, PASSWORD)
db = firebase.database()
users = db.child("debug").get(user['idToken'])
print(users.val())
