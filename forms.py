from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from flask import flash


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=14)]
    )

    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In!")


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=14)]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=5),
            EqualTo("confirmpassword", message=("Passwords do not match")),
        ],
    )
    confirmpassword = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message=("Passwords do not match")),
        ],
    )

    submit = SubmitField("Sign Up!")


class DeleteAccountForm(FlaskForm):
    yes = SubmitField("Yes!")
    no = SubmitField("No, go back!")
