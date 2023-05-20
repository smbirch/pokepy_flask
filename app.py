from flask import Flask, render_template, request, redirect, flash, url_for, session

from forms import LoginForm, RegistrationForm, DeleteAccountForm
import controller
import database
import main


app = Flask(__name__)

app.config["SECRET_KEY"] = "temporarysecretkey"


print(
    "\nStrong Pokémon, weak Pokémon, that is only the foolish perception of people. Truly skilled trainers should try to win with their favorites.\n"
)
database.create_db()


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
    userdata = session.get("userdata")

    if userdata == None:
        return redirect(url_for("index"))

    username = userdata.get("username")
    teamobject = userdata.get("teamobject")
    return render_template("userhome.html", username=username, teamobject=teamobject)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        userobject = controller.create_user(username, password)

        if userobject == "duplicateaccounterror":
            flash(f"There is already a user with that username!", "success")
            return redirect(url_for("register"))

        flash(f"Account created for {form.username.data}!", "success")
        set_userdata_session(username)
        print(f"\n***{form.username.data} has registered!***\n")

        return redirect(url_for("userhome", username=username))

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

        set_userdata_session(username)
        print(f"\n***{form.username.data} has logged in***\n")
        return redirect(url_for("userhome"))

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/random_team", methods=["POST"])
def random_team():
    userdata = session.get("userdata")
    username = userdata.get("username")
    userid = userdata.get("userid")

    teamobject = controller.get_team(userid)
    controller.make_random_team(teamobject)
    set_userdata_session(username)
    return redirect(url_for("userhome", username=username))


@app.route("/delete_team", methods=["POST"])
def delete_team():
    userdata = session.get("userdata")
    username = userdata.get("username")
    userid = userdata.get("userid")

    teamobject = controller.get_team(userid)
    database.Team.delete_team(teamobject)
    set_userdata_session(username)
    return redirect(url_for("userhome", username=username))


def set_userdata_session(username):
    userobject = controller.get_user_session(username)
    teamobject = controller.get_team(userobject.userid)

    userdata = {
        "username": userobject.username,
        "userid": userobject.userid,
        "teamobject": {
            "mon1": teamobject.mon1,
            "mon2": teamobject.mon2,
            "mon3": teamobject.mon3,
            "mon4": teamobject.mon4,
            "mon5": teamobject.mon5,
            "mon6": teamobject.mon6,
        },
    }
    session["userdata"] = userdata


@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    form = DeleteAccountForm()

    userdata = session.get("userdata")

    if userdata == None:
        return redirect(url_for("index"))

    username = userdata.get("username")

    if request.method == "POST":
        if form.yes.data:
            # Delete the user's account and log them out
            if controller.delete_account(username) == "delete_error":
                flash(f"There was an error deleting the account")
                return redirect(url_for("userhome", username=username))
            else:
                session.clear()
                flash(f"{username}'s account was deleted")

                return redirect(url_for("index"))
        elif form.no.data:
            return redirect(url_for("userhome", username=username))

    else:
        return render_template("delete_account.html", form=form)
