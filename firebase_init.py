import json
import os
from dotenv import load_dotenv
from firebase_admin import credentials


def init_firebase():
    load_dotenv()
    # Fetch Firebase credentials from environment variable
    firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')


    if not firebase_credentials:
        raise Exception("Firebase credentials are not set in environment variables.")

    try:
        # Remove any extra quotes and decode the JSON string
        firebase_credentials = firebase_credentials.strip("'\"")
        cred_dict = json.loads(firebase_credentials)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Received value: {firebase_credentials}")
        raise

    # Initialize Firebase using the credentials from the environment
    cred = credentials.Certificate(cred_dict)
    return cred


