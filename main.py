from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_frozen import Freezer
from db_instance import get_db
from models.editorial_board_model import EditorialRole
from services import editorial_service, journal_service, mail_service, page_service, social_link_service
from routes import Routes
from paths import Paths



#! DB instance
db = get_db();


#! Flask app
app = Flask(__name__)
app.secret_key = 'journalwebx8949328001'
# app.config['SERVER_NAME'] = 'localhost:5000'

#! Fetch all journals 
all_journals = journal_service.get_all_journals()


@app.route(Routes.HOME)
def Home():

    #! Fetch the content for the home page
    doc_id = "8061MAE63evqpTPdIvlz"
    content = page_service.get_page(doc_id)

    #! Fetch editorial board members
    all_editorial_board_members = editorial_service.get_all_editorial_board_members()
    editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.EDITOR]
    associate_editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.ASSOCIATE_EDITOR]
    chief_editor_name = [member.name for member in all_editorial_board_members if member.role == EditorialRole.CHIEF_EDITOR]


    #! return the home page with the content and the editors' data
    return render_template(Paths.INDEX, content=content, editors=editors_list, chief_editor_name=chief_editor_name, associate_editors=associate_editors_list)


@app.route(Routes.CURRENT_ISSUE)
def currissue():
    # Fetch articles from Firestore
    articles_ref = db.collection('articles')
    articles = articles_ref.stream()
    
    # Extract titles from articles
    article_data = [
        {
            'title': article.to_dict().get('title', 'No Title'),
            'authors': ', '.join([author.get('name', 'Unknown') for author in article.to_dict().get('authors', [])]),
            'createdAt': article.to_dict().get('createdAt', 'Unknown Date'),
            'image': article.to_dict().get('image', None),
            'pdf': article.to_dict().get('pdf', None)
        } for article in articles
    ]

    return render_template(Paths.CURRENT_ISSUE, articles=article_data)

@app.route(Routes.ARTICLE_DETAILS)
def article_details():
    # Fetch articles from Firestore
    articles_ref = db.collection('articles')
    articles = articles_ref.stream()
    
    # Extract detailed information from articles
    article_data = [
        {
            'title': article.to_dict().get('title', 'No Title'),
            'documentType': article.to_dict().get('documentType', 'Unknown Type'),
            'authors': ', '.join([author.get('name', 'Unknown') for author in article.to_dict().get('authors', [])]),
            'pdf': article.to_dict().get('pdf', None),
            'abstractString': article.to_dict().get('abstractString', 'No abstract available'),
            'keywords': article.to_dict().get('keywords', []),
            'mainSubjects': article.to_dict().get('mainSubjects', []),
            'references': article.to_dict().get('references', []),
            'image': article.to_dict().get('image', None),
        } for article in articles
    ]

    return render_template(Paths.ARTICLE_DETAILS, articles=article_data)

@app.route(Routes.BY_ISSUE)
def byissue():
    return render_template(Paths.BY_ISSUE)

@app.route(Routes.ARCHIVE)
def archive():
    return render_template(Paths.ARCHIVE)

@app.route(Routes.ABOUT_JOURNAL)
def about_journal():
    doc_id = "s7zN7Ce9XCsEOP63CtUb"
    return render_template(Paths.ABOUT_JOURNAL, content=page_service.get_page(doc_id))

@app.route(Routes.AIM_AND_SCOPE)
def aimnscope():
    doc_id = "w45mTbOFFg54c7HSU4Ay"    
    return render_template(Paths.AIM_AND_SCOPE, content=page_service.get_page(doc_id))
    
@app.route(Routes.EDITORIAL_BOARD)
def editboard():
    # Fetch editorial board data from Firestore
    editorial_board_ref = db.collection('editorialBoard').stream()
    
    # Extract specific data from the fetched documents
    board_members = [{
        'role': member.to_dict().get('role', 'Unknown Role'),
        'name': member.to_dict().get('name', 'Unknown Name'),
        'institution': member.to_dict().get('institution', 'Unknown Institution'),
        'email': member.to_dict().get('email', 'Unknown Email')
    } for member in editorial_board_ref]

    # Define a custom sort order for roles
    role_priority = {'Chief Editor': 1, 'Associate Editor': 2, 'Editor': 3}
    
    # Sort the members by their role based on priority
    board_members.sort(key=lambda x: role_priority.get(x['role'], 999))
    
    return render_template(Paths.EDITORIAL_BOARD, board_members=board_members)

@app.route(Routes.PUBLICATION_ETHICS)
def pubethics():
    doc_id = "W6bSKPFmVh6ejZMVxsWr"
    return render_template(Paths.PUBLICATION_ETHICS, content=page_service.get_page(doc_id))

    
@app.route(Routes.PEER_REVIEW_PROCESS)
def peerpro():

    doc_id = "CZpNkvbYXi0Ae5RQASJp"
    return render_template(Paths.PEER_REVIEW_PROCESS, content=page_service.get_page(doc_id))
    

@app.route(Routes.INDEXING_AND_ABSTRACTING)
def indnabs():
    return render_template(Paths.INDEXING_AND_ABSTRACTING)

@app.route(Routes.SUBMIT_ONLINE_PAPER)
def subon():
    return render_template(Paths.SUBMIT_ONLINE_PAPER)

@app.route(Routes.TOPICS)
def topic():
    doc_id = "QoxjARRGKlL7BKUtcpQM"
    return render_template(Paths.TOPICS, content=page_service.get_page(doc_id))

@app.route(Routes.AUTHOR_GUIDELINES)
def authgl():

    doc_id = "4OJKeKoJ3LStfoEU88Hu"
    return render_template(Paths.AUTHOR_GUIDELINES, content=page_service.get_page(doc_id))

@app.route(Routes.COPYRIGHT_FORM)
def crform():
    return render_template(Paths.COPYRIGHT_FORM)
@app.route(Routes.CHECK_PAPER_STATUS)
def checkpapstat():
    return render_template(Paths.CHECK_PAPER_STATUS)
@app.route(Routes.MEMBERSHIP)
def mship():
    return render_template(Paths.MEMBERSHIP)
@app.route(Routes.SUBMIT_MANUSCRIPT)
def submitmanscr():
    return render_template(Paths.SUBMIT_MANUSCRIPT)
@app.route(Routes.REVIEWER)
def reviewer():

    doc_id = "GiZuANsNXJTxZdt8jQbR"
    return render_template(Paths.REVIEWER, content=page_service.get_page(doc_id))

@app.route(Routes.CONTACT, methods=['GET', 'POST'])
def ContactUs():

    doc_id = "ylhdV31SBbX3exH9olKj"
    content = page_service.get_page(doc_id)
    
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        questiontype = request.form.get("questiontype")
        message = request.form.get("message")


        mail_service.send_email(name, email, phone, subject, questiontype, message)

        flash('Your message has been successfully submitted!', 'success')
        return redirect(url_for('ContactUs'))
    
    return render_template(Paths.CONTACT, content=content)


@app.route(Routes.GET_SOCIAL_LINKS)
def get_social_links():
    return social_link_service.get_social_links()


freezer = Freezer(app)

if __name__ == "__main__":
    # Comment this out when freezing
    app.run(debug=True)

    # Uncomment this to generate the static files
    freezer.freeze()
    