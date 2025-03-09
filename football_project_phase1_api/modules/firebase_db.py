#firebase_db.py.py

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("football-b34a3-firebase-adminsdk-fbsvc-fa34f1117a.json")  # Replace with your key file
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_session(user_id, session_data):
    """Saves the user's training session data to Firebase."""
    doc_ref = db.collection("sessions").document(user_id)
    doc_ref.set(session_data)
    return {"message": "Session saved successfully!"}

def get_session(user_id):
    """Retrieves the user's previous training session data."""
    doc_ref = db.collection("sessions").document(user_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else {"message": "No session data found."}

