from flask import Flask, render_template, request, redirect, flash, url_for

import controller
from forms import LoginForm, RegistrationForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "temporarysecretkey"


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


@app.route("/userhome")
def userhome():
    return render_template("userhome.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        userobject = controller.create_user(username, password)

        if userobject == "duplicateaccounterror":
            print("There is already a user with that username!")
            print(userobject)
            flash(f"There is already a user with that username!", "success")

            return redirect(url_for("register"))

        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("userhome"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        userobject = controller.get_user(username, password)
        print(userobject)
        if userobject == "404":
            flash(f"No account found for {form.username.data}")
            return redirect(url_for("login"))

        return redirect(url_for("userhome"))

    return render_template("login.html", title="Login", form=form)
