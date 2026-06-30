from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Passwort", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Passwort", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField(
        "Passwort bestätigen",
        validators=[DataRequired(), EqualTo("password", message="Passwörter stimmen nicht überein.")],
    )
    submit = SubmitField("Registrieren")


class ProfileEditForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    rolle = SelectField(
        "Status",
        choices=[("suchend", "Auf Wohnungssuche"), ("anbietend", "Bietet ein Inserat an")],
    )
    alter = IntegerField("Alter")
    beruf = StringField("Beruf", validators=[Length(max=120)])
    stadt = StringField("Stadt", validators=[Length(max=120)])
    nationalitaet = StringField("Nationalität", validators=[Length(max=120)])
    budget_min = IntegerField("Minimales Budget")
    budget_max = IntegerField("Maximales Budget")
    raucher = BooleanField("Raucher")
    haustiere = BooleanField("Haustiere")
    sauberkeit = IntegerField("Sauberkeit (1-5)")
    bio = TextAreaField("Bio")
    foto = FileField("Bild (JPEG)", validators=[FileAllowed(["jpg", "jpeg"], "Nur JPEG-Bilder erlaubt.")])
    submit = SubmitField("Profil speichern")


class ListingForm(FlaskForm):
    title = StringField("Titel", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Beschreibung", validators=[DataRequired()])
    rent = IntegerField("Miete (CHF)", validators=[DataRequired()])
    deposit = IntegerField("Depot")
    location = StringField("Ort / Adresse", validators=[DataRequired(), Length(max=200)])
    room_size = IntegerField("Zimmergröße (m²)")
    available_from = DateField("Verfügbar ab", format="%Y-%m-%d")
    furnished = BooleanField("Möbliert")
    pets_allowed = BooleanField("Haustiere erlaubt")
    smoking_allowed = BooleanField("Rauchen erlaubt")
    flatmates = IntegerField("Anzahl Mitbewohner")
    foto = FileField("Bild (JPEG)", validators=[FileAllowed(["jpg", "jpeg"], "Nur JPEG-Bilder erlaubt.")])
    submit = SubmitField("Inserat speichern")
