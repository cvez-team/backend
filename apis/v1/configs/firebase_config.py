import os
import firebase_admin as admin
from firebase_admin import firestore
from firebase_admin import storage


# Initialize credentials
cred_dict = {
    "type": "service_account",
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.environ.get('FIREBASE_CLIENT_EMAIL')}",
    "universe_domain": "googleapis.com"
}
cred = admin.credentials.Certificate(cred_dict)

# Initialize the app with a service account, granting admin privileges
app = admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client(app)

# Initialize Storage client
bucket = storage.bucket(
    name=f"{os.environ.get('FIREBASE_PROJECT_ID')}.appspot.com", app=app)
