from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_frozen import Freezer
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import sys

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'journalwebx8949328001'

# Fetch Firebase credentials from environment variable
firebase_credentials = os.environ.get('FIREBASE_CREDENTIALS')


if not firebase_credentials:
    raise Exception("Firebase credentials are not set in environment variables.")

try:
    # Try to remove any extra quotes that might be causing issues
    firebase_credentials = firebase_credentials.strip("'\"")
    cred_dict = json.loads(firebase_credentials)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    print(f"Received value (first 50 chars): {firebase_credentials[:50]}")
    raise

# Initialize Firebase using the credentials from the environment
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

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

    doc_id = "s7zN7Ce9XCsEOP63CtUb"
    doc_ref = db.collection('pages').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return render_template('screens/journal_info/about_jrnl.html', content=content)
    else:
        return "Document not found", 404

@app.route("/aimandscope.html")
def aimnscope():

    doc_id = "w45mTbOFFg54c7HSU4Ay"
    doc_ref = db.collection('pages').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return render_template('screens/journal_info/aimandscope.html', content=content)
    else:
        return "Document not found", 404
@app.route("/editorial_board.html")
def editboard():
    # Fetch editorial board data from Firestore
    editorial_board_ref = db.collection('editorialBoard').order_by('createdAt', direction='ASCENDING')
    editorial_board = editorial_board_ref.stream()
    
    # Extract specific data from the fetched documents
    board_members = [{
        'role': member.to_dict().get('role', 'Unknown Role'),
        'name': member.to_dict().get('name', 'Unknown Name'),
        'institution': member.to_dict().get('institution', 'Unknown Institution'),
        'email': member.to_dict().get('email', 'Unknown Email')
    } for member in editorial_board]
    
    return render_template('screens/journal_info/editorial_board.html', board_members=board_members)
@app.route("/publication_ethics.html")
def pubethics():


    doc_id = "W6bSKPFmVh6ejZMVxsWr"
    doc_ref = db.collection('pages').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return render_template('screens/journal_info/publication_ethics.html', content=content)
    else:
        return "Document not found", 404
    
@app.route("/peerrevpro.html")
def peerpro():

    doc_id = "CZpNkvbYXi0Ae5RQASJp"
    doc_ref = db.collection('pages').document(doc_id)
    doc = doc_ref.get()
    
    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return render_template('screens/journal_info/peerrevpro.html', content=content)
    else:
        return "Document not found", 404
@app.route("/indandabs.html")
def indnabs():
    return render_template('screens/journal_info/indandabs.html')
@app.route("/subonpaper.html")
def subon():
    return render_template('screens/for_author/subonpaper.html')
@app.route("/topics.html")
def topic():

    doc_id = "QoxjARRGKlL7BKUtcpQM"
    doc_ref = db.collection('pages').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return render_template('screens/for_author/topics.html', content=content)
    else:
        return "Document not found", 404
@app.route("/author_gl.html")
def authgl():

    doc_id = "4OJKeKoJ3LStfoEU88Hu"
    doc_ref = db.collection('pages').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return render_template('screens/for_author/author_gl.html', content=content)
    else:
        return "Document not found", 404
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

    doc_id = "GiZuANsNXJTxZdt8jQbR"
    doc_ref = db.collection('pages').document(doc_id)
    doc = doc_ref.get()

    if doc.exists:
        # Extract 'content' field from the document
        content = doc.to_dict().get('content', '')
        return render_template('pages/reviewer.html', content=content)
    else:
        return "Document not found", 404
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

@app.route("/get_social_links")
def get_social_links():
    # Fetch social links from Firestore
    social_links_ref = db.collection('socialLinks')
    social_links = social_links_ref.stream()

    # Extract name and url from each document
    social_links_data = [
        {
            'url': link.to_dict().get('url', '#')
        } for link in social_links
    ]

    # Return the data as JSON
    return jsonify(social_links_data)


freezer = Freezer(app)

if __name__ == "__main__":
    # Comment this out when freezing
    app.run(debug=True)

    # Uncomment this to generate the static files
    freezer.freeze()

