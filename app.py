import logging
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session,
    request,
)
from logging.config import dictConfig

import forms
import controller
import database

# logging
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s >> %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "applogger": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/userlogs.log",
                "maxBytes": 1000000,
                "backupCount": 3,
                "formatter": "default",
            },
            "httplogger": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/httplogs.log",
                "maxBytes": 1000000,
                "backupCount": 3,
                "formatter": "default",
            },
            "errorlogger": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "logs/errorlogs.log",
                "maxBytes": 1000000,
                "backupCount": 3,
                "formatter": "default",
            },
        },
        # "root": {"level": "WARNING", "handlers": ["console"]},
        "loggers": {
            "userlogs": {
                "level": "INFO",
                "handlers": ["applogger"],
                "propagate": False,
            },
            "httplogs": {
                "level": "INFO",
                "handlers": ["httplogger"],
                "propagate": False,
            },
            "errorlogs": {
                "level": "ERROR",
                "handlers": ["errorlogger"],
                "propagate": False,
            },
        },
    }
)

userlogs = logging.getLogger("userlogs")
httplogs = logging.getLogger("httplogs")
errorlogs = logging.getLogger("errorlogs")

app = Flask(__name__)

app.config["SECRET_KEY"] = "temporarysecretkey"

database.create_db()


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


def set_mondata_session(monname):
    monobject = controller.get_single_mon(monname)
    if monobject == None:
        return "mon_not_found"

    mondata = {
        "monid": monobject.id,
        "monname": monobject.name,
        "height": monobject.height,
        "weight": monobject.weight,
        "type": monobject.montype,
        "sprite": monobject.sprite,
    }

    session["mondata"] = mondata


@app.route("/", methods=["GET", "POST"])
def index():
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            flash("All fields are required")
            return render_template("/", form=form)
        else:
            return redirect("userhome")

    return render_template("index.html")


@app.route("/userhome", methods=["GET", "POST"])
def userhome():
    form = forms.GetMonForm()

    userdata = session.get("userdata")
    if userdata == None:
        return redirect(url_for("index"))

    username = userdata.get("username")
    teamobject = userdata.get("teamobject")
    return render_template(
        "userhome.html", username=username, teamobject=teamobject, form=form
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        userobject = controller.create_user(username, password)

        if userobject == "duplicateaccounterror":
            userlogs.info(f"error: duplicate account: {username}")
            flash(f"There is already a user with that username!")
            return redirect(url_for("register"))

        flash(f"Account created for {form.username.data}!")
        set_userdata_session(username)

        userlogs.info(f"USER:{form.username.data} - EVENT:register")

        return redirect(url_for("userhome", username=username))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        userobject = controller.get_user(username, password)
        if userobject == "404":
            userlogs.info(f"No account found for {form.username.data} - 404")
            flash(f"No account found for {form.username.data}")
            return redirect(url_for("login"))

        elif userobject == "401":
            userlogs.info(f"Invalid password for USER:{form.username.data} - 401")
            flash(f"Invalid username or password")
            return redirect(url_for("login"))

        set_userdata_session(username)

        userlogs.info(f"USER:{form.username.data} - EVENT:login")

        return redirect(url_for("userhome"))

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    userdata = session.get("userdata")
    if userdata == None:
        return redirect(url_for("index"))

    username = userdata.get("username")
    userlogs.info(f"USER:{username} - EVENT:logout")

    session.clear()
    return redirect(url_for("index"))


@app.route("/delete_team", methods=["POST"])
def delete_team():
    userdata = session.get("userdata")
    username = userdata.get("username")
    userid = userdata.get("userid")

    teamobject = controller.get_team(userid)
    if teamobject == "500":
        flash("Error deleting team")
        return redirect(url_for("userhome"))

    if database.Team.delete_team(teamobject) == "500":
        flash("Error deleting team")
        return redirect(url_for("userhome"))

    set_userdata_session(username)
    userlogs.info(f"USER:{username} - EVENT:delete_team")

    return redirect(request.referrer)


@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    form = forms.DeleteAccountForm()
    userdata = session.get("userdata")

    if userdata == None:
        return redirect(url_for("index"))

    username = userdata.get("username")

    if request.method == "POST":
        if form.yes.data:
            userlogs.info(f"USER:{form.username.data} - EVENT:delete_account")

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


@app.route("/get_mon", methods=["GET", "POST"])
def get_mon():
    form = forms.GetMonForm()
    userdata = session.get("userdata")

    if userdata == None:
        return redirect(url_for("index"))

    if form.validate_on_submit():
        monname = form.monname.data
        if monname == "None":
            flash("There was a problem with this request. Please try again")
            return redirect(url_for("userhome"))

        if set_mondata_session(monname) == "mon_not_found":
            flash(f"Could not find {monname}. Check your spelling and try again")
            return redirect(url_for("get_mon", form=form))

        return redirect(url_for("mon_info"))

    return render_template("get_mon.html", form=form)


@app.route("/all_mons")
def all_mons():
    userdata = session.get("userdata")

    if userdata == None:
        return redirect(url_for("index"))

    form = forms.GetMonForm()

    monslist = controller.get_all_mons()
    if monslist == "error":
        flash("There was an error getting this list")
        return redirect(url_for("userhome"))
    return render_template("all_mons.html", monslist=monslist, form=form)


@app.route("/mon_info")
def mon_info():
    form = forms.GetMonForm()

    userdata = session.get("userdata")
    if userdata == None:
        return redirect(url_for("index"))

    mondata = session.get("mondata")

    return render_template("mon_info.html", mondata=mondata, form=form)


@app.route("/random_team", methods=["POST"])
def random_team():
    userdata = session.get("userdata")
    username = userdata.get("username")
    userid = userdata.get("userid")

    teamobject = controller.get_team(userid)
    controller.make_random_team(teamobject)
    set_userdata_session(username)

    userlogs.info(f"USER:{username} - EVENT:random_team")
    return redirect(request.referrer)


@app.route("/edit_team", methods=["GET", "POST"])
def edit_team():
    form = forms.GetMonForm()
    userdata = session.get("userdata")
    if userdata == None:
        return redirect(url_for("index"))

    username = userdata.get("username")
    teamobject = userdata.get("teamobject")
    return render_template(
        "edit_team.html", username=username, teamobject=teamobject, form=form
    )


@app.route("/add_pokemon", methods=["POST"])
def add_pokemon():
    form = forms.GetMonForm()
    userdata = session.get("userdata")
    if userdata == None:
        return redirect(url_for("index"))

    mondata = session.get("mondata")
    if mondata == None:
        return redirect(url_for("/edit_team"))

    username = userdata.get("username")
    userid = userdata.get("userid")
    monname = mondata.get("monname")

    monobject = controller.get_single_mon(monname)
    teamobject = controller.get_team(userid)
    if database.Team.add_mon_to_team(teamobject, monobject) == "428_team_full":
        flash(f"Your team is already full!")
        return render_template("mon_info.html", mondata=mondata, form=form)

    set_userdata_session(username)

    return redirect(url_for("edit_team"))


@app.route("/remove_pokemon", methods=["POST"])
def remove_pokemon():
    userdata = session.get("userdata")
    if userdata == None:
        return redirect(url_for("index"))
    userid = userdata.get("userid")
    username = userdata.get("username")

    teamobject = controller.get_team(userid)
    pokemon_pos = request.form.get("pokemon_pos")

    controller.update_team(teamobject, int(pokemon_pos), "None")
    set_userdata_session(username)

    return redirect(url_for("edit_team"))


# for logging http requests
@app.after_request
def logAfterRequest(response):
    httplogs.info(
        "path: %s | method: %s | status: %s | size: %s",
        request.path,
        request.method,
        response.status,
        response.content_length,
    )

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
