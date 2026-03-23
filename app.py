from flask import Flask, render_template, request, redirect

app = Flask(__name__)

notes = {}  # словарь для записей

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/notes", methods=["GET", "POST"])
def notes_page():
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")

        if title and text:
            notes[title] = text

        return redirect("/notes")

    return render_template("notes.html", notes=notes)

if __name__ == "__main__":
    app.run(debug=True)