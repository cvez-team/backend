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
    "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
    "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": "googleapis.com"
}
cred = admin.credentials.Certificate(cred_dict)

# Initialize the app with a service account, granting admin privileges
app = admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client(app)

# Initialize Storage client
bucket = storage.bucket(
    name=f"gs:/{os.environ.get('FIREBASE_PROJECT_ID')}.appspot.com", app=app)
