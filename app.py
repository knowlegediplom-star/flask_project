from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)


# ---------- МОДЕЛИ ----------

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    text = db.Column(db.Text)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    token = db.Column(db.String(200))   #  ДОБАВИЛИ ТОКЕН


# ---------- ГЛАВНЫЕ СТРАНИЦЫ ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/home")
def home_page():
    return render_template("home.html")


# ---------- ЗАМЕТКИ ----------

@app.route("/notes", methods=["GET", "POST"])
def notes_page():
    #  ПРОВЕРКА ТОКЕНА
    token = request.args.get("token")
    user = User.query.filter_by(token=token).first()

    if not user:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title")
        subtitle = request.form.get("subtitle")
        text = request.form.get("text")

        if title and text:
            new_note = Note(title=title, subtitle=subtitle, text=text)
            db.session.add(new_note)
            db.session.commit()

        return redirect(f"/notes?token={token}")  #  сохраняем токен

    notes = Note.query.all()
    return render_template("notes.html", notes=notes)


# ---------- РЕГИСТРАЦИЯ ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        #  СОЗДАЁМ ТОКЕН
        token = str(uuid.uuid4())

        user = User(username=username, email=email, password=password, token=token)
        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------- ЛОГИН ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            return redirect(f"/notes?token={user.token}")  #  ПЕРЕДАЁМ ТОКЕН
        else:
            return "Ошибка входа"

    return render_template("login.html")


# ---------- ЗАПУСК ----------

if __name__ == "__main__":
    app.run(debug=True)