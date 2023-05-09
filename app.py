from flask import Flask, render_template, request, redirect, flash, url_for, session
from forms import LoginForm, RegistrationForm

import controller
import main


app = Flask(__name__)

app.config["SECRET_KEY"] = "temporarysecretkey"


main.main()


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash("All fields are required")
            return render_template("/", form=form)
        else:
            return redirect("userhome")

    return render_template("index.html")


@app.route("/userhome", methods=["GET", "POST"])
def userhome():
    username = session.get("usersession")
    userobject = controller.get_user_session(username)
    userteam = controller.get_team(userobject)
    return render_template("userhome.html", userobject=userobject, userteam=userteam)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        userobject = controller.create_user(username, password)

        if userobject == "duplicateaccounterror":
            print("There is already a user with that username!")
            flash(f"There is already a user with that username!", "success")
            return redirect(url_for("register"))

        flash(f"Account created for {form.username.data}!", "success")
        session["usersession"] = userobject.username
        return redirect(url_for("userhome", userobject=userobject))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        userobject = controller.get_user(username, password)
        if userobject == "404":
            flash(f"No account found for {form.username.data}")
            return redirect(url_for("login"))

        elif userobject == "401":
            flash(f"Invalid username or password")
            return redirect(url_for("login"))

        session["usersession"] = userobject.username
        print(f"***{form.username.data} has logged in***")
        return redirect(url_for("userhome", userobject=userobject))

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
