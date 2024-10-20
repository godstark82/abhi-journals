from typing import List, Optional
from flask import Flask, g, render_template, request, redirect, url_for, flash
from db_instance import get_db
from models.editorial_board_model import EditorialRole
from models.journal_model import JournalModel
from services import editorial_service, journal_service, mail_service, page_service, social_link_service, user_service
from routes import Routes
from paths import Paths
from waitress import serve
from google.api_core.exceptions import InvalidArgument
from services.mail_service import send_email



#! Flask app
app = Flask(__name__)
app.secret_key = 'journalwebx8949328001'
# app.config['SERVER_NAME'] = 'abhijournals.com'
app.config['SERVER_NAME'] = 'localhost:5000'

db = get_db()

#
#! Fetch all journals 
all_journals = journal_service.get_all_journals()
journal: JournalModel = None

def get_journal(all_journals: List[JournalModel], subdomain: str = "main") -> Optional[JournalModel]:
    journal = None
    for journalItem in all_journals:
        if journalItem.domain == subdomain:
            journal = journalItem
            break

    if not journal:
        return None
    journal_details = journal_service.get_journal(journal.id)
    return journal_details

def load_journal(subdomain):
    if not hasattr(g, 'journal'):
        g.journal = get_journal(all_journals, subdomain)
    return g.journal


# Add a route for the root domain
@app.route(Routes.HOME)
def root_home():
    journal = load_journal("main")
    volumes_count = journal_service.get_all_volumes_count()
    issues_count = journal_service.get_all_issues_count()
    articles_count = journal_service.get_all_articles_count()
    users_count = user_service.get_all_users_count()
    return render_template('home/index.html', journal=journal, all_journals=all_journals, volumes_count=volumes_count, issues_count=issues_count, articles_count=articles_count, users_count=users_count)

@app.route(Routes.CONTACT, methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Optionally add phone and questiontype if needed

        # Send the email using the send_email function from mail_service
        send_email(name, email, None, subject, None, message)

        flash('Your message has been successfully submitted!', 'success')
        return redirect(url_for('contact'))

    return render_template(Paths.INDEX)


@app.route(Routes.HOME, subdomain='<subdomain>')
def home(subdomain):
    # Attempt to find the corresponding journal for the subdomain
    journal = load_journal(subdomain)
    # Fetch the content for the home page
    content = page_service.get_page('Home', journal.id)
    # Fetch editorial board members
    all_editorial_board_members = editorial_service.get_all_editorial_board_members(journal.id)
    editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.EDITOR]
    associate_editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.ASSOCIATE_EDITOR]
    chief_editor_names = [member.name for member in all_editorial_board_members if member.role == EditorialRole.CHIEF_EDITOR]

    # Fetch articles from Firestore
    articles = journal.get_all_artcles_of_active_issues()
    users_count = user_service.get_all_users_count()

    # Return the home page with the fetched content and editorial board data
    return render_template(
        Paths.INDEX,
        articles=articles,
        users_count=users_count,
        content=content,
        editors=editors_list,
        chief_editor_name=chief_editor_names,
        associate_editors=associate_editors_list,
        journal=journal,
        subdomain=subdomain
    )



@app.route(Routes.CURRENT_ISSUE, subdomain='<subdomain>')
def current_issue(subdomain):
    # Find the journal that matches the subdomain
    journal = load_journal(subdomain)
    error_message = None

    # Fetch active volumes for the current journal
    active_volume_ids = [vol.id for vol in journal.get_all_active_volumes()]
    if not active_volume_ids:
        error_message = "No active volumes found for this journal"
    
    # Fetch active issue IDs based on active volumes for the current journal
    active_issue_ids = [issue.id for issue in journal.get_all_active_issues()]
    if not active_issue_ids:
        error_message = "No active issues found for this journal"

    # Fetch articles from Firestore
    articles = journal.get_all_artcles_of_active_issues()
    
    # Extract titles from articles
    return render_template(Paths.CURRENT_ISSUE, articles=articles, error_message=error_message, journal = journal, subdomain=subdomain  )


@app.route(Routes.BY_ISSUE, subdomain='<subdomain>')
def by_issue(subdomain):
    # Find the journal that matches the subdomain
    journal = load_journal(subdomain)
    if not journal.volumes:
        # If there are no volumes, return an empty list of issues
        return render_template(Paths.BY_ISSUE, issues=[], error_message="No issues found for this journal.", journal = journal, subdomain=subdomain)

    try:    
        issues = journal.get_all_issues()
        # Sort issues by issueNumber in descending order
        issues.sort(key=lambda x: x.issue_number, reverse=True)     
        return render_template(Paths.BY_ISSUE, issues=issues, error_message=None, journal=journal, subdomain=subdomain)
    
    except InvalidArgument:
        # Handle the case where there are no issues
        return render_template(Paths.BY_ISSUE, issues=[], journal = journal, error_message="No issues found for this journal.", subdomain=subdomain)

@app.route(Routes.ARCHIVE, subdomain='<subdomain>')
def archive(subdomain): 
    # Find the journal that matches the subdomain
    journal = load_journal(subdomain)

    journal.volumes.sort(key=lambda x: x.volume_number, reverse=True)

    if not journal.volumes:
        error_message = "No volumes with articles found for this journal."
    else:
        error_message = None
    # Pass all volumes to the template
    return render_template(Paths.ARCHIVE, journal=journal, error_message=error_message, subdomain=subdomain )

@app.route(Routes.ISSUE_DETAILS + '/<issue_id>/articles/' , subdomain='<subdomain>')
def issue_details(subdomain, issue_id):
    journal = load_journal(subdomain)
    articles = journal.get_all_articles_of_issue(issue_id)
    return render_template(Paths.ISSUE_DETAILS, articles=articles, journal=journal, subdomain= subdomain)


@app.route(Routes.ARTICLE_DETAILS + '/<article_id>', subdomain='<subdomain>')
def article_details(subdomain, article_id):
    journal = load_journal(subdomain)
    article = journal.get_article_by_id(article_id)
    return render_template(Paths.ARTICLE_DETAILS, journal=journal, article=article, subdomain=subdomain)


# New route to handle issues for a specific volume
@app.route('/volume/<volume_id>/issues', subdomain='<subdomain>')
def volume_issues(subdomain, volume_id):
    # Fetch the issues for the volume that contain articles
    journal = load_journal(subdomain)
    issues = journal.get_all_issues_of_volume(volume_id)
    if not issues:
        return render_template(Paths.VOLUME_ISSUES, issues=[], error_message="No issues with articles found for this volume.")
    # return volume_id
    return render_template(Paths.VOLUME_ISSUES, issues=issues, journal=journal, subdomain=subdomain)


@app.route(Routes.ABOUT_JOURNAL, subdomain='<subdomain>')
def about_journal(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.ABOUT_JOURNAL, content=page_service.get_page('About Journal',journal.id), journal = journal)

@app.route(Routes.AIM_AND_SCOPE, subdomain='<subdomain>')
def aim_and_scope(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.AIM_AND_SCOPE, content=page_service.get_page('Aim and Scope', journal.id), journal = journal)
    
@app.route(Routes.EDITORIAL_BOARD, subdomain='<subdomain>')
def editorial_board(subdomain):
    journal = load_journal(subdomain)
    eb_members = editorial_service.get_all_editorial_board_members(journal.id)
    return render_template(Paths.EDITORIAL_BOARD, board_members=eb_members, journal = journal)

@app.route(Routes.PUBLICATION_ETHICS, subdomain='<subdomain>')
def publication_ethics(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.PUBLICATION_ETHICS, content=page_service.get_page('Publication Ethics',journal.id), journal = journal)

    
@app.route(Routes.PEER_REVIEW_PROCESS, subdomain='<subdomain>')
def peer_review_process(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.PEER_REVIEW_PROCESS, content=page_service.get_page('Peer Review Process',journal.id), journal = journal)
    

@app.route(Routes.INDEXING_AND_ABSTRACTING, subdomain='<subdomain>')
def indexing_and_abstracting(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.INDEXING_AND_ABSTRACTING, journal = journal)

@app.route(Routes.SUBMIT_ONLINE_PAPER, subdomain='<subdomain>')
def submit_online_paper(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.SUBMIT_ONLINE_PAPER, journal = journal)

@app.route(Routes.TOPICS, subdomain='<subdomain>')
def topic(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.TOPICS, content=page_service.get_page('Topics',journal.id), journal = journal)

@app.route(Routes.AUTHOR_GUIDELINES, subdomain='<subdomain>')
def author_guidelines(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.AUTHOR_GUIDELINES, content=page_service.get_page('Author Guidelines',journal.id), journal = journal)

@app.route(Routes.COPYRIGHT_FORM, subdomain='<subdomain>')
def copyright_form(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.COPYRIGHT_FORM, journal = journal)


@app.route(Routes.MEMBERSHIP, subdomain='<subdomain>')
def membership(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.MEMBERSHIP, journal = journal)
@app.route(Routes.SUBMIT_MANUSCRIPT, subdomain='<subdomain>')
def submit_manuscript(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.SUBMIT_MANUSCRIPT, journal = journal)
@app.route(Routes.REVIEWER, subdomain='<subdomain>')
def reviewer(subdomain):
    journal = load_journal(subdomain)
    return render_template(Paths.REVIEWER, content=page_service.get_page('Reviewer',journal.id), journal = journal)

@app.route(Routes.CHECK_PAPER_STATUS, subdomain='<subdomain>', methods=['GET', 'POST'])
def check_paper_status(subdomain, article=None):
    article = None
    if request.method == 'POST':
        registration_id = request.form['registration-id']
        article = journal_service.get_article_by_id(registration_id)
        journal = load_journal(subdomain)
        return render_template(Paths.CHECK_PAPER_STATUS, journal = journal, article=article)
    
    journal = load_journal(subdomain)
    return render_template(Paths.CHECK_PAPER_STATUS, journal = journal, article=article)


@app.route(Routes.CONTACT, subdomain='<subdomain>', methods=['GET', 'POST'])
def contact_us(subdomain):    
    journal = load_journal(subdomain)
    content = page_service.get_page('Contact Us',journal.id)
    
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        questiontype = request.form.get("questiontype")
        message = request.form.get("message")


        mail_service.send_email(name, email, phone, subject, questiontype, message)

        flash('Your message has been successfully submitted!', 'success')
        return redirect(url_for('contact_us', subdomain=subdomain))
    
    return render_template(Paths.CONTACT, content=content, journal = journal, subdomain=subdomain)


@app.route(Routes.GET_SOCIAL_LINKS, subdomain='<subdomain>')
def get_social_links(subdomain):
    journal = load_journal(subdomain)
    return social_link_service.get_social_links()




mode = "prod"

if __name__ == "__main__":
    # Comment this out when freezing
    if mode == "dev":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app, host='0.0.0.0', port=5000, threads=4)