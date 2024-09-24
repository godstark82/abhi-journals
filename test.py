import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyBhdyPrsSHO9jVIngsXZ3sRPgKqaqqXPJQ",
  "authDomain": "journal-3c895.firebaseapp.com",
  "projectId": "journal-3c895",
  "storageBucket": "journal-3c895.appspot.com",
  "messagingSenderId": "1095141627347",
  "appId": "1:1095141627347:web:d490b3b836137703734b26"
};

firebase = pyrebase.initialize_app(firebaseConfig)

""" Auth  """
auth = firebase.auth()

def signup():
  email = input("Email: ")
  password = input("Password: ")
  try:
    user = auth.create_user_with_email_and_password(email, password)
    print(user)
  except:
    print("Error")

def login():
  email = input("Email: ")
  password = input("Password: ")
  try:
    user = auth.sign_in_with_email_and_password(email, password)
    print(user)
  except:
    print("Error")

signup()