
# if not firebase_credentials:
#     raise Exception("Firebase credentials are not set in environment variables.")

# try:
#     # Try to remove any extra quotes that might be causing issues
#     firebase_credentials = firebase_credentials.strip("'\"")
#     cred_dict = json.loads(firebase_credentials)
# except json.JSONDecodeError as e:
#     print(f"Error decoding JSON: {e}")
#     print(f"Received value (first 50 chars): {firebase_credentials[:50]}")
#     raise