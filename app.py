from flask import Flask, render_template, redirect, request, url_for, session
from datetime import timedelta

class User:
    def __init__(self, id, fullname, username, password):
        self.fullname = fullname
        self.username = username
        self.id = id
        self.password = password

users = []

app = Flask(__name__)
app.secret_key = "secretkeythatverysecret"
app.permanent_session_lifetime = timedelta(minutes = 10)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.permanent = True
    if len(users) != 0:
        count = users[len(users) - 1].id + 1
    else:
        count = 0   

    if request.method == "POST":
        full_name = request.form["fullname"]
        user_name = request.form["username"]
        pin = request.form["password"]
        if full_name and user_name and pin:
            users.append(User(id=count, fullname=full_name, username=user_name, password=pin))
            session["user_id"] = users[len(users) - 1].username
            return redirect(url_for("profile", usr=users[len(users) - 1].username))
        
        return redirect(url_for("register"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.permanent = True
    if request.method == "POST":
        session.pop("user_id", None)
        username = request.form["username"]
        password = request.form["password"]
        person = []
        for user in users:
            if user.username == username:
                person.append(user)
                break

        if person and person[0].password == password:
            session["user_id"] = person[0].username
            return redirect(url_for("profile", usr=person[0].username))
        
        return redirect(url_for("login"))
    if "user_id" in session:
        return redirect(url_for("profile", usr=session["user_id"]))
    return render_template("login.html")

@app.route("/profile/<usr>")
def profile(usr):
    full_name = ""
    if session.get("user_id"):
        for person in users:
            if usr == person.username:
                full_name = person.fullname
                break
        if usr == session["user_id"]:
            return render_template("profile.html", name=full_name)
        else:
            return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

@app.route("/anakanjing", methods=["GET", "POST"])
def registrants():
    return render_template("registrants.html", USERS=users)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))
    
