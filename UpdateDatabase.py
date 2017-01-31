"""
Python script to update user database of NCBSinfo app
Database is hosted on Firebase Real Time Database

You will need following files (which are untracked from version control for security)
secrets/credentials.py # Contains all database urls, api keys and credentials
user_data/UserRegistration # Contains user registration data
secrets/service_file.json # Your admin service file downloaded from project console

Script uses pyrebase library : https://github.com/thisbejim/Pyrebase
"""

import pyrebase

from Models import UserModel
from secrets.credentials import *

config = {
    "apiKey": API_KEY,
    "authDomain": AUTH_DOMAIN,  # ProjectID.firebaseapp.com
    "databaseURL": DATABASE_URL,
    "storageBucket": STORAGE_BUCKET,  # projectId.appspot.com
    "serviceAccount": "secrets/service_file.json"  # Service file
}

# Initialize firebase with config
firebase = pyrebase.initialize_app(config)
# Get database reference
db = firebase.database()

# Get user data
user_data = []
with open("user_data/UserRegistration.csv", "r") as f:
    for line in f:
        e = line.strip().split(",")
        user_data.append(UserModel(e))

# Remove header
del user_data[0]

# Take only new registration
user_data = [x for x in user_data if x.external_code.lower() == "newuser"]
# Sort by timestamp
user_data.sort(key=lambda x: x.timestamp)

user_dic = {}
# Create unique list
for u in user_data:
    assert isinstance(u, UserModel)
    # If there are more than 1 instance of newUser, take first one
    if u.email not in user_dic:
        user_dic[u.email] = u

# Get database of users
online_users = db.child("authEmails").get()
# Print statistics
print(len(user_dic))
print(len(online_users.each()))

# List of users with problems in account database
conflicted_users = []
# Final confirmed users
confirmed_users = []

for user in online_users.each():
    try:
        # Check if UID is same as recorded
        if user.key() == user_dic.get(user.val()).firebase_id:
            confirmed_users.append(user_dic.get(user.val()))
            pass
        else:
            # Print conflicted user accounts
            print(user_dic.get(user.val()).email)
    except AttributeError:
        # Collect data for problematic user accounts
        conflicted_users.append([user.key(), user.val()])

# Print stats
print("Total of %d confirmed users and %d problematic users found " % (len(confirmed_users), len(conflicted_users)))

for u in confirmed_users:
    assert isinstance(u, UserModel)
    data = {"creation_date": u.creation_timestamp, "uid": u.firebase_id}
    db.child("debug").child("users").child(u.email_path).update(data)
