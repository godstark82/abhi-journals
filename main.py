from flask import Flask, render_template
from flask_frozen import Freezer
app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html')

@app.route("/archive.html")
def archive():
    return render_template('archive.html')

@app.route("/journal_info.html")
def journal():
    return render_template('journal_info.html')

@app.route("/contact.html")
def Contact():
    return render_template('contact.html')

freezer = Freezer(app)
if __name__ == "__main__":
    app.run(debug=True)