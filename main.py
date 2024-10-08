from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_frozen import Freezer
from db_instance import get_db
from models.editorial_board_model import EditorialRole
from services import editorial_service, journal_service, mail_service, page_service, social_link_service
from routes import Routes
from paths import Paths
from waitress import serve
from google.api_core.exceptions import InvalidArgument



#! DB instance
db = get_db();


#! Flask app
app = Flask(__name__)
app.secret_key = 'journalwebx8949328001'
app.config['SERVER_NAME'] = 'abhijournals.com'

#! Fetch all journals 
all_journals = journal_service.get_all_journals()


currentsubdomain = 'main'

@app.route(Routes.HOME, subdomain='<subdomain>')
def Home(subdomain):
    global journal_data

    # Find the journal that matches the subdomain
    journal_data = next((journal for journal in all_journals if journal.domain == subdomain), None)
    currentsubdomain = subdomain
    if not journal_data:
        # If no matching journal is found, you might want to handle this case
        # For example, redirect to a default page or show an error
        return "Journal not found", 404

    #! Fetch the content for the home page
    doc_id = "8061MAE63evqpTPdIvlz"
    content = page_service.get_page(doc_id)

    #! Fetch editorial board members
    all_editorial_board_members = editorial_service.get_all_editorial_board_members()
    editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.EDITOR]
    associate_editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.ASSOCIATE_EDITOR]
    chief_editor_name = [member.name for member in all_editorial_board_members if member.role == EditorialRole.CHIEF_EDITOR]
    
    #! return the home page with the content and the editors' data
    return render_template(Paths.INDEX, content=content, editors=editors_list, chief_editor_name=chief_editor_name, associate_editors=associate_editors_list, journal=journal_data, subdomain=currentsubdomain)

# Add a route for the root domain
# @app.route(Routes.HOME)
# def root_home():
#     return redirect(url_for('Home', subdomain='main'))


@app.route(Routes.CURRENT_ISSUE, subdomain='<subdomain>')
def currissue(subdomain):
    # Find the journal that matches the subdomain
    journal = next((journal for journal in all_journals if journal.domain == subdomain), None)
    if not journal:
        error_message = "Journal not found"
        return render_template(Paths.CURRENT_ISSUE, articles=[], error_message=error_message), 404

    # Fetch active volumes for the current journal
    active_volumes = db.collection('volumes').where('isActive', '==', True).where('journalId', '==', journal.id).stream()
    active_volume_ids = [vol.id for vol in active_volumes]

    if not active_volume_ids:
        error_message = "No active volumes found for this journal"
        return render_template(Paths.CURRENT_ISSUE, articles=[], error_message=error_message), 404
    
    # Fetch active issue IDs based on active volumes for the current journal
    active_issues = db.collection('issues').where('isActive', '==', True).where('volumeId', 'in', active_volume_ids).stream()
    active_issue_ids = [issue.id for issue in active_issues]

    if not active_issue_ids:
        error_message = "No active issues found for this journal"
        return render_template(Paths.CURRENT_ISSUE, articles=[], error_message=error_message), 404

    # Fetch articles from Firestore
    articles_ref = db.collection('articles').where('issueId', 'in', active_issue_ids)
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

    return render_template(Paths.CURRENT_ISSUE, articles=article_data, error_message=None)

@app.route(Routes.ARTICLE_DETAILS, subdomain='<subdomain>')
def article_details(subdomain):
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


@app.route(Routes.BY_ISSUE, subdomain='<subdomain>')
def byissue(subdomain):
    # Find the journal that matches the subdomain
    journal = next((journal for journal in all_journals if journal.domain == subdomain), None)
    if not journal:
        return render_template(Paths.BY_ISSUE, issues=[], error_message="Journal not found.")

    # Fetch all volumes for the current journal
    volumes_ref = db.collection('volumes').where('journalId', '==', journal.id)
    volumes = volumes_ref.stream()
    volume_ids = [volume.id for volume in volumes]

    if not volume_ids:
        # If there are no volumes, return an empty list of issues
        return render_template(Paths.BY_ISSUE, issues=[], error_message="No issues found for this journal.")

    try:
        # Fetch all issues for the current journal's volumes
        issues_ref = db.collection('issues').where('volumeId', 'in', volume_ids)
        issues = issues_ref.stream()
        
        # Extract title, issueNumber, and isActive from issues
        issue_data = [
            {
                'title': issue.to_dict().get('title', 'Untitled Issue'),
                'issueNumber': issue.to_dict().get('issueNumber', 'N/A'),
                'isActive': issue.to_dict().get('isActive', False)
            } for issue in issues
        ]   
        
        # Sort issues by issueNumber in descending order
        issue_data.sort(key=lambda x: x['issueNumber'], reverse=True)
        
        return render_template(Paths.BY_ISSUE, issues=issue_data, error_message=None)
    
    except InvalidArgument:
        # Handle the case where there are no issues
        return render_template(Paths.BY_ISSUE, issues=[], error_message="No issues found for this journal.")

@app.route(Routes.ARCHIVE, subdomain='<subdomain>')
def archive(subdomain):
    # Find the journal that matches the subdomain
    journal = next((journal for journal in all_journals if journal.domain == subdomain), None)
    if not journal:
         return render_template(Paths.ARCHIVE, active_volumes=[], journal=None, error_message="Journal not found.")
    
    # Fetch volumes for the current journal
    volumes_ref = db.collection('volumes').where('isActive', '==', True).where('journalId', '==', journal.id)
    volumes = volumes_ref.stream()

    # Collect the volume data
    active_volumes = [
        {
            'volumeNumber': volume.to_dict().get('volumeNumber', 'N/A'),
            'title': volume.to_dict().get('title', 'Untitled'),
            'createdAt': volume.to_dict().get('createdAt', 'Unknown Date'),
            'isActive': volume.to_dict().get('isActive', False)
        }
        for volume in volumes
    ]
     # Sort volumes by volumeNumber in descending order
    active_volumes.sort(key=lambda x: x['volumeNumber'], reverse=True)

    if not active_volumes:
        error_message = "No active volumes found for this journal."
    else:
        error_message = None

    # Pass the active volumes to the template
    return render_template(Paths.ARCHIVE, active_volumes=active_volumes, journal=journal,error_message=error_message)

@app.route(Routes.ABOUT_JOURNAL, subdomain='<subdomain>')
def about_journal(subdomain):
    doc_id = "s7zN7Ce9XCsEOP63CtUb"
    return render_template(Paths.ABOUT_JOURNAL, content=page_service.get_page(doc_id))

@app.route(Routes.AIM_AND_SCOPE, subdomain='<subdomain>')
def aimnscope(subdomain):
    doc_id = "w45mTbOFFg54c7HSU4Ay"    
    return render_template(Paths.AIM_AND_SCOPE, content=page_service.get_page(doc_id))
    
@app.route(Routes.EDITORIAL_BOARD, subdomain='<subdomain>')
def editboard(subdomain):
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

@app.route(Routes.PUBLICATION_ETHICS, subdomain='<subdomain>')
def pubethics(subdomain):
    doc_id = "W6bSKPFmVh6ejZMVxsWr"
    return render_template(Paths.PUBLICATION_ETHICS, content=page_service.get_page(doc_id))

    
@app.route(Routes.PEER_REVIEW_PROCESS, subdomain='<subdomain>')
def peerpro(subdomain):

    doc_id = "CZpNkvbYXi0Ae5RQASJp"
    return render_template(Paths.PEER_REVIEW_PROCESS, content=page_service.get_page(doc_id))
    

@app.route(Routes.INDEXING_AND_ABSTRACTING, subdomain='<subdomain>')
def indnabs(subdomain):
    return render_template(Paths.INDEXING_AND_ABSTRACTING)

@app.route(Routes.SUBMIT_ONLINE_PAPER, subdomain='<subdomain>')
def subon(subdomain):
    return render_template(Paths.SUBMIT_ONLINE_PAPER)

@app.route(Routes.TOPICS, subdomain='<subdomain>')
def topic(subdomain):
    doc_id = "QoxjARRGKlL7BKUtcpQM"
    return render_template(Paths.TOPICS, content=page_service.get_page(doc_id))

@app.route(Routes.AUTHOR_GUIDELINES, subdomain='<subdomain>')
def authgl(subdomain):

    doc_id = "4OJKeKoJ3LStfoEU88Hu"
    return render_template(Paths.AUTHOR_GUIDELINES, content=page_service.get_page(doc_id))

@app.route(Routes.COPYRIGHT_FORM, subdomain='<subdomain>')
def crform(subdomain):
    return render_template(Paths.COPYRIGHT_FORM)
@app.route(Routes.CHECK_PAPER_STATUS, subdomain='<subdomain>')
def checkpapstat(subdomain):
    return render_template(Paths.CHECK_PAPER_STATUS)
@app.route(Routes.MEMBERSHIP, subdomain='<subdomain>')
def mship(subdomain):
    return render_template(Paths.MEMBERSHIP)
@app.route(Routes.SUBMIT_MANUSCRIPT, subdomain='<subdomain>')
def submitmanscr(subdomain):
    return render_template(Paths.SUBMIT_MANUSCRIPT)
@app.route(Routes.REVIEWER, subdomain='<subdomain>')
def reviewer(subdomain):

    doc_id = "GiZuANsNXJTxZdt8jQbR"
    return render_template(Paths.REVIEWER, content=page_service.get_page(doc_id))

@app.route(Routes.CONTACT, subdomain='<subdomain>', methods=['GET', 'POST'])
def ContactUs(subdomain):    

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


@app.route(Routes.GET_SOCIAL_LINKS, subdomain='<subdomain>')
def get_social_links(subdomain):
    return social_link_service.get_social_links()


freezer = Freezer(app)

# mode = "prod"

if __name__ == "__main__":
    # Comment this out when freezing
    # if mode == "dev":
        app.run(host='0.0.0.0', port=5000, debug=True)
    # else:
    #     serve(app, host='0.0.0.0', port=5000, threads=4)

    # Uncomment this to generate the static files
    # freezer.freeze()