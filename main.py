from typing import List, Optional
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from db_instance import get_db
from models.editorial_board_model import EditorialRole
from models.journal_model import JournalModel
from services import editorial_service, journal_service, mail_service, page_service, social_link_service
from routes import Routes
from paths import Paths
from waitress import serve
from google.api_core.exceptions import InvalidArgument



#! Flask app
app = Flask(__name__)
app.secret_key = 'journalwebx8949328001'
# app.config['SERVER_NAME'] = 'abhijournals.com'
app.config['SERVER_NAME'] = 'abhijournals.com'

db = get_db()

#
#! Fetch all journals 
all_journals = journal_service.get_all_journals()
journal: JournalModel = None

def get_journal(all_journals: List[JournalModel], subdomain: str = "main")-> Optional[JournalModel]:
    journal = None
    for journalItem in all_journals:
        if journalItem.domain == subdomain:
            journal = journalItem
            break

    if not journal:
        return None
    journal_details = journal_service.get_journal(journal.id)
    return journal_details



# Add a route for the root domain
@app.route(Routes.HOME)
def root_home():
    return redirect(url_for('Home', subdomain='main'))


@app.route(Routes.HOME, subdomain='<subdomain>')
def Home(subdomain):
    # Attempt to find the corresponding journal for the subdomai
    journal = get_journal(all_journals, subdomain)

    currentsubdomain = subdomain

    # Fetch the content for the home page
    doc_id = "8061MAE63evqpTPdIvlz"
    content = page_service.get_page(doc_id)

    # Fetch editorial board members
    all_editorial_board_members = editorial_service.get_all_editorial_board_members()
    editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.EDITOR]
    associate_editors_list = [member.name for member in all_editorial_board_members if member.role == EditorialRole.ASSOCIATE_EDITOR]
    chief_editor_names = [member.name for member in all_editorial_board_members if member.role == EditorialRole.CHIEF_EDITOR]

    # Fetch articles from Firestore
    articles = journal.get_all_artcles_of_active_issues()

    # Return the home page with the fetched content and editorial board data
    return render_template(
        Paths.INDEX,
        articles=articles,
        content=content,
        editors=editors_list,
        chief_editor_name=chief_editor_names,
        associate_editors=associate_editors_list,
        journal=journal,
        subdomain=currentsubdomain
    )




@app.route(Routes.CURRENT_ISSUE, subdomain='<subdomain>')
def currissue(subdomain):
    # Find the journal that matches the subdomain
    journal = get_journal(all_journals, subdomain = subdomain)
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

    return render_template(Paths.CURRENT_ISSUE, articles=articles, error_message=error_message, subdomain=subdomain)


@app.route(Routes.BY_ISSUE, subdomain='<subdomain>')
def byissue(subdomain):
    # Find the journal that matches the subdomain
    journal = get_journal(all_journals, subdomain)
    if not journal.volumes:
        # If there are no volumes, return an empty list of issues
        return render_template(Paths.BY_ISSUE, issues=[], error_message="No issues found for this journal.", subdomain=subdomain)

    try:    
        issues = journal.get_all_issues()
        # Sort issues by issueNumber in descending order
        issues.sort(key=lambda x: x.issue_number, reverse=True)     
        return render_template(Paths.BY_ISSUE, issues=issues, error_message=None, subdomain=subdomain)
    
    except InvalidArgument:
        # Handle the case where there are no issues
        return render_template(Paths.BY_ISSUE, issues=[], subdomain=subdomain, error_message="No issues found for this journal.")

@app.route(Routes.ARCHIVE, subdomain='<subdomain>')
def archive(subdomain): 
    # Find the journal that matches the subdomain
    for journalItem in all_journals:
        if journalItem.domain == subdomain:
            journal = journalItem
            break

    journal = journal_service.get_journal(journal.id)
    journal.volumes.sort(key=lambda x: x.volume_number, reverse=True)

    if not journal.volumes:
        error_message = "No volumes with articles found for this journal."
    else:
        error_message = None
    # Pass all volumes to the template
    return render_template(Paths.ARCHIVE, journal=journal, error_message=error_message, subdomain=subdomain)

@app.route(Routes.ISSUE_DETAILS + '/<issue_id>/articles/' , subdomain='<subdomain>')
def issue_details(subdomain, issue_id):
    journal = get_journal(all_journals, subdomain)
    articles = journal.get_all_articles_of_issue(issue_id)
    return render_template(Paths.ISSUE_DETAILS, articles=articles, subdomain=subdomain)


@app.route(Routes.ARTICLE_DETAILS + '/<article_id>', subdomain='<subdomain>')
def article_details(subdomain, article_id):
    journal = get_journal(all_journals, subdomain)
    article = journal.get_article_by_id(article_id)
    return render_template(Paths.ARTICLE_DETAILS, subdomain=subdomain, article=article)


# New route to handle issues for a specific volume
@app.route('/volume/<volume_id>/issues', subdomain='<subdomain>')
def volume_issues(subdomain, volume_id):
    # Fetch the issues for the volume that contain articles
    journal = get_journal(all_journals, subdomain)
    issues = journal.get_all_issues_of_volume(volume_id)
    if not issues:
        return render_template(Paths.VOLUME_ISSUES, issues=[], error_message="No issues with articles found for this volume.")
    # return volume_id
    return render_template(Paths.VOLUME_ISSUES, issues=issues, subdomain=subdomain)


@app.route(Routes.ABOUT_JOURNAL, subdomain='<subdomain>')
def about_journal(subdomain):
    doc_id = "s7zN7Ce9XCsEOP63CtUb"
    return render_template(Paths.ABOUT_JOURNAL, content=page_service.get_page(doc_id), subdomain=subdomain)

@app.route(Routes.AIM_AND_SCOPE, subdomain='<subdomain>')
def aimnscope(subdomain):
    doc_id = "w45mTbOFFg54c7HSU4Ay"    
    return render_template(Paths.AIM_AND_SCOPE, content=page_service.get_page(doc_id), subdomain=subdomain)
    
@app.route(Routes.EDITORIAL_BOARD, subdomain='<subdomain>')
def editboard(subdomain):
    eb_members = editorial_service.get_all_editorial_board_members()
    return render_template(Paths.EDITORIAL_BOARD, board_members=eb_members, subdomain=subdomain)

@app.route(Routes.PUBLICATION_ETHICS, subdomain='<subdomain>')
def pubethics(subdomain):
    doc_id = "W6bSKPFmVh6ejZMVxsWr"
    return render_template(Paths.PUBLICATION_ETHICS, content=page_service.get_page(doc_id), subdomain=subdomain)

    
@app.route(Routes.PEER_REVIEW_PROCESS, subdomain='<subdomain>')
def peerpro(subdomain):

    doc_id = "CZpNkvbYXi0Ae5RQASJp"
    return render_template(Paths.PEER_REVIEW_PROCESS, content=page_service.get_page(doc_id), subdomain=subdomain)
    

@app.route(Routes.INDEXING_AND_ABSTRACTING, subdomain='<subdomain>')
def indnabs(subdomain):
    return render_template(Paths.INDEXING_AND_ABSTRACTING, subdomain=subdomain)

@app.route(Routes.SUBMIT_ONLINE_PAPER, subdomain='<subdomain>')
def subon(subdomain):
    return render_template(Paths.SUBMIT_ONLINE_PAPER, subdomain=subdomain)

@app.route(Routes.TOPICS, subdomain='<subdomain>')
def topic(subdomain):
    doc_id = "QoxjARRGKlL7BKUtcpQM"
    return render_template(Paths.TOPICS, content=page_service.get_page(doc_id), subdomain=subdomain)

@app.route(Routes.AUTHOR_GUIDELINES, subdomain='<subdomain>')
def authgl(subdomain):

    doc_id = "4OJKeKoJ3LStfoEU88Hu"
    return render_template(Paths.AUTHOR_GUIDELINES, content=page_service.get_page(doc_id), subdomain=subdomain)

@app.route(Routes.COPYRIGHT_FORM, subdomain='<subdomain>')
def crform(subdomain):
    return render_template(Paths.COPYRIGHT_FORM, subdomain=subdomain)
@app.route(Routes.CHECK_PAPER_STATUS, subdomain='<subdomain>')
def checkpapstat(subdomain):
    return render_template(Paths.CHECK_PAPER_STATUS, subdomain=subdomain)
@app.route(Routes.MEMBERSHIP, subdomain='<subdomain>')
def mship(subdomain):
    return render_template(Paths.MEMBERSHIP, subdomain=subdomain)
@app.route(Routes.SUBMIT_MANUSCRIPT, subdomain='<subdomain>')
def submitmanscr(subdomain):
    return render_template(Paths.SUBMIT_MANUSCRIPT, subdomain=subdomain)
@app.route(Routes.REVIEWER, subdomain='<subdomain>')
def reviewer(subdomain):

    doc_id = "GiZuANsNXJTxZdt8jQbR"
    return render_template(Paths.REVIEWER, content=page_service.get_page(doc_id), subdomain=subdomain)

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
    
    return render_template(Paths.CONTACT, content=content, subdomain=subdomain)


@app.route(Routes.GET_SOCIAL_LINKS, subdomain='<subdomain>')
def get_social_links(subdomain):
    return social_link_service.get_social_links()




mode = "dev"

if __name__ == "__main__":
    # Comment this out when freezing
    if mode == "dev":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app, host='0.0.0.0', port=5000, threads=4)