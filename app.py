from flask import Flask, render_template, request, redirect, flash, url_for

import controller
from forms import LoginForm, RegistrationForm


app = Flask(__name__)

app.config["SECRET_KEY"] = "temporarysecretkey"


@app.route("/", methods=["GET", "POST"])
def index():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit() == False:
            flash("All fields are required")
            return render_template("/", form=form)
        else:
            username = form.username.data
            password = form.password.data
            userobject = controller.get_user(username, password)
            print(userobject)
            return redirect("userhome")

    return render_template("index.html")


@app.route("/userhome")
def userhome():
    return render_template("userhome.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("userhome"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)
