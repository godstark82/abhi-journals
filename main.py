from flask import Flask, render_template
from flask_frozen import Freezer
app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html')

@app.route("/category.html")
def Category():
    return render_template('category.html')

@app.route("/single.html")
def Single():
    return render_template('single.html')

@app.route("/contact.html")
def Contact():
    return render_template('contact.html')

freezer = Freezer(app)
if __name__ == "__main__":
    app.run(debug=True)