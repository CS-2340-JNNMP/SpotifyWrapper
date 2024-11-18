import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
from dotenv import load_dotenv

load_dotenv()
# Path to your service account key JSON file
FIREBASE_CREDENTIALS = os.getenv('FIREBASE_KEY_PATH')

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_app = firebase_admin.initialize_app(cred)

# Firestore client
firestore_db = firestore.client()
