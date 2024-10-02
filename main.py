from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_frozen import Freezer
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'journalwebx8949328001'

# Fetch Firebase credentials from environment variable
firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')

if firebase_credentials:
    # Convert the environment variable JSON string back to a dictionary
    cred_dict = json.loads(firebase_credentials)

    # Initialize Firebase using the credentials from the environment
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

    db = firestore.client()
else:
    raise Exception("Firebase credentials are not set in environment variables.")

@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/current_issue.html")
def currissue():
    # Fetch articles from Firestore
    articles_ref = db.collection('articles')
    articles = articles_ref.stream()
    
    # Extract titles from articles
    article_data = [
        {
            'title': article.to_dict().get('title', 'No Title'),
            'authors': article.to_dict().get('authors', 'Unknown Author'),
            'createdAt': article.to_dict().get('createdAt', 'Unknown Date'),
            'image': article.to_dict().get('image', None),
            'pdf': article.to_dict().get('pdf', None)
        } for article in articles
    ]

    return render_template('screens/browse/current_issue.html', articles=article_data)

@app.route("/article_details.html")
def article_details():
    # Fetch articles from Firestore
    articles_ref = db.collection('articles')
    articles = articles_ref.stream()
    
    # Extract detailed information from articles
    article_data = [
        {
            'title': article.to_dict().get('title', 'No Title'),
            'documentType': article.to_dict().get('documentType', 'Unknown Type'),
            'authors': article.to_dict().get('authors', []),
            'pdf': article.to_dict().get('pdf', None),
            'abstractString': article.to_dict().get('abstractString', 'No abstract available'),
            'keywords': article.to_dict().get('keywords', []),
            'mainSubjects': article.to_dict().get('mainSubjects', []),
            'references': article.to_dict().get('references', []),
            'image': article.to_dict().get('image', None),
        } for article in articles
    ]

    return render_template('screens/browse/article_details.html', articles=article_data)

@app.route("/by_issue.html")
def byissue():
    return render_template('screens/browse/by_issue.html')

@app.route("/archive_2024.html")
def archive():
    return render_template('screens/archivee/archive_2024.html')

@app.route("/about_jrnl.html")
def about_journal():
    return render_template('screens/journal_info/about_jrnl.html')
@app.route("/aimandscope.html")
def aimnscope():
    return render_template('screens/journal_info/aimandscope.html')
@app.route("/editorial_board.html")
def editboard():
    return render_template('screens/journal_info/editorial_board.html')
@app.route("/publication_ethics.html")
def pubethics():
    return render_template('screens/journal_info/publication_ethics.html')
@app.route("/peerrevpro.html")
def peerpro():
    return render_template('screens/journal_info/peerrevpro.html')
@app.route("/indandabs.html")
def indnabs():
    return render_template('screens/journal_info/indandabs.html')
@app.route("/subonpaper.html")
def subon():
    return render_template('screens/for_author/subonpaper.html')
@app.route("/topics.html")
def topic():
    return render_template('screens/for_author/topics.html')
@app.route("/author_gl.html")
def authgl():
    return render_template('screens/for_author/author_gl.html')
@app.route("/copyrightform.html")
def crform():
    return render_template('screens/for_author/copyrightform.html')
@app.route("/checkpaperstats.html")
def checkpapstat():
    return render_template('screens/for_author/checkpaperstats.html')
@app.route("/membership.html")
def mship():
    return render_template('screens/for_author/membership.html')
@app.route("/submanuscript.html")
def submitmanscr():
    return render_template('pages/submanuscript.html')
@app.route("/reviewer.html")
def reviewer():
    return render_template('pages/reviewer.html')
@app.route("/contact.html", methods=['GET', 'POST'])
def ContactUs():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        questiontype = request.form.get("questiontype")
        message = request.form.get("message")

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "subject": subject,
            "questiontype": questiontype,
            "message": message
      }

        db.collection("contact").add(data)
        flash('Your message has been successfully submitted!', 'success')
        return redirect(url_for('ContactUs'))
    return render_template('contact.html')

freezer = Freezer(app)

if __name__ == "__main__":
    # Comment this out when freezing
    app.run(debug=True)

    # Uncomment this to generate the static files
    freezer.freeze()

