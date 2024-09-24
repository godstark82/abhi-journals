from flask import Flask, render_template
from flask_frozen import Freezer
app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html')
@app.route("/current_issue.html")
def current_issue():
    return render_template('screens/browse/current_issue.html')
@app.route("/by_issue.html")
def by_issue():
    return render_template('screens/browse/by_issue.html')

@app.route("/archive.html")
def archive():
    return render_template('archive.html')
@app.route("/archive_2024.html")
def archive_2024():
    return render_template('screens/archivee/archive_2024.html')

@app.route("/about_jrnl.html")
def about_jrnl():
    return render_template('screens/journal_info/about_jrnl.html')
@app.route("/aimandscope.html")
def aimandscope():
    return render_template('screens/journal_info/aimandscope.html')
@app.route("/editorial_board.html")
def editorial_board():
    return render_template('screens/journal_info/editorial_board.html')
@app.route("/publication_ethics.html")
def publication_ethics():
    return render_template('screens/journal_info/publication_ethics.html')
@app.route("/peerrevpro.html")
def peerrevpro():
    return render_template('screens/journal_info/peerrevpro.html')
@app.route("/indandabs.html")
def indandabs():
    return render_template('screens/journal_info/indandabs.html')
@app.route("/subonpaper.html")
def subonpaper():
    return render_template('screens/for_author/subonpaper.html')
@app.route("/topics.html")
def topics():
    return render_template('screens/for_author/topics.html')
@app.route("/author_gl.html")
def author_gl():
    return render_template('screens/for_author/author_gl.html')
@app.route("/copyrightform.html")
def copyrightform():
    return render_template('screens/for_author/copyrightform.html')
@app.route("/checkpaperstats.html")
def checkpaperstats():
    return render_template('screens/for_author/checkpaperstats.html')
@app.route("/membership.html")
def membership():
    return render_template('screens/for_author/membership.html')
@app.route("/submanuscript.html")
def submanuscript():
    return render_template('pages/submanuscript.html')
@app.route("/reviewer.html")
def reviewer():
    return render_template('pages/reviewer.html')
@app.route("/regasrev.html")
def regasrev():
    return render_template('screens/join_us/regasrev.html')
@app.route("/regasbm.html")
def regasbm():
    return render_template('screens/join_us/regasbm.html')

@app.route("/contact.html")
def Contact():
    return render_template('contact.html')

freezer = Freezer(app)
if __name__ == "__main__":
    app.run(debug=True)