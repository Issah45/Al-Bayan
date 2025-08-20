from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "K1YS1R"

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route("/lessons")
def lessons():
    con = sqlite3.connect("lessons.db")
    cur = con.cursor()
    cur.execute("SELECT LessonName, VideoFile FROM lessons")
    rows = cur.fetchall()
    cur.execute("SELECT LessonName, Contents FROM textlessons")
    rowst = cur.fetchall()
    print(rowst)
    return render_template("lessons.html", lessons=rows, textlessons=rowst)

@app.route("/lessonupload", methods=["GET", "POST"])
def lessonupload():
    if request.method == "POST":
        con = sqlite3.connect("lessons.db")
        cur = con.cursor()
        name = request.form["name"]
        video = request.form["video"]
        type = request.form["type"]
        content = request.form["content"]

        if type == "v":
            cur.execute(f"INSERT INTO lessons(LessonName, VideoFile) values('{name}', '{video}')")
            con.commit()
        elif type == "t":
            cur.execute(f"INSERT INTO textlessons(LessonName, Contents) values('{name}', '{content}')")
            con.commit()

        return redirect(url_for("lessons"))
    return render_template("lessonupload.html")

@app.route("/")
def home():
    #session.uname = "Anonymous"
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        con = sqlite3.connect("accounts.db")
        cur = con.cursor()
        username = request.form["username"]
        password = request.form["password"]

        #cur.execute(f"INSERT INTO accounts(username, password) values('{username}', '{password}')")
        session.uname = username

        return render_template("user.html", username=username, password=password)
    return render_template("signup.html")

@app.route("/user")
def user(username, password):
    return render_template("user.html")


app.run()
