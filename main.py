from flask import Flask, render_template
from flask_frozen import Freezer
app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/current_issue.html")
def currissue():
    return render_template('screens/browse/current_issue.html')
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
@app.route("/contact.html")
def ContactUs():
    return render_template('contact.html')

freezer = Freezer(app)
if __name__ == "__main__":
    app.run(debug=True)