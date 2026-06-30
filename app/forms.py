from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DateTimeLocalField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
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
        "Passwort bestaetigen",
        validators=[DataRequired(), EqualTo("password", message="Passwoerter stimmen nicht ueberein.")],
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
    kanton = StringField("Kanton", validators=[DataRequired(), Length(max=50)])
    ort = StringField("Ort", validators=[DataRequired(), Length(max=200)])
    strasse = StringField("Strasse", validators=[Length(max=200)])
    room_size = IntegerField("Zimmergroesse (m2)")
    available_from = DateField("Verfuegbar ab", format="%Y-%m-%d")
    furnished = BooleanField("Moebliert")
    pets_allowed = BooleanField("Haustiere erlaubt")
    smoking_allowed = BooleanField("Rauchen erlaubt")
    flatmates = IntegerField("Anzahl Mitbewohner")
    foto = FileField("Bild (JPEG)", validators=[FileAllowed(["jpg", "jpeg"], "Nur JPEG-Bilder erlaubt.")])
    submit = SubmitField("Inserat speichern")


class ApplicationForm(FlaskForm):
    nachricht = TextAreaField("Nachricht (optional)", validators=[Length(max=2000)])
    submit = SubmitField("Für Inserat bewerben")


class AppointmentForm(FlaskForm):
    scheduled_at = DateTimeLocalField("Wunschtermin", format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    nachricht = TextAreaField("Nachricht (optional)", validators=[Length(max=2000)])
    submit = SubmitField("Besichtigung anfragen")


class MessageForm(FlaskForm):
    body = TextAreaField("Nachricht", validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField("Senden")


class ConfirmForm(FlaskForm):
    """Leeres Formular nur für CSRF-geschützte POST-Aktionen (z. B. Ablehnen)."""

    submit = SubmitField("OK")
