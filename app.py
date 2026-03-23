from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    text = db.Column(db.Text)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/notes", methods=["GET", "POST"])
def notes_page():
    if request.method == "POST":
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        text = request.form.get("text")

        if title and text:
            new_note = Note(title=title, subtitle=subtitle, text=text)
            db.session.add(new_note)
            db.session.commit()

        return redirect("/notes")

    notes = Note.query.all()
    return render_template("notes.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)