from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


# ---------- МОДЕЛИ ----------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    token = db.Column(db.String(200))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer)


# ---------- ГЛАВНАЯ ----------

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


# ---------- РЕГИСТРАЦИЯ ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

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
            return redirect(f"/dashboard?token={user.token}")
        else:
            return "Ошибка входа"

    return render_template("login.html")


# ---------- ЛИЧНЫЙ КАБИНЕТ ----------

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    token = request.args.get("token")
    user = User.query.filter_by(token=token).first()

    if not user:
        return redirect("/login")

    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")

        post = Post(title=title, text=text, user_id=user.id)
        db.session.add(post)
        db.session.commit()

        return redirect(f"/dashboard?token={token}")

    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template("dashboard.html", posts=posts, token=token)


# ---------- УДАЛЕНИЕ ----------

@app.route("/delete/<int:id>")
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")


# ---------- ЗАПУСК ----------

if __name__ == "__main__":
    app.run(debug=True)