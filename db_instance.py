import firebase_admin
from firebase_admin import credentials, firestore
from firebase_init import init_firebase

class FirestoreDB:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            firebase_app = firebase_admin.initialize_app(credential=init_firebase())
            cls._instance = firestore.client()
        return cls._instance

# Create a convenience function to get the db instance
def get_db():
    return FirestoreDB.get_instance()
