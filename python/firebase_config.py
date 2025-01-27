import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("python/firebase/aacopilot-55872-firebase-adminsdk-c25fg-d3a0ecf48e.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()