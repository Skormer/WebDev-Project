from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, DateTimeLocalField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, URL


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
    hobbies = TextAreaField("Hobbys", validators=[Length(max=1000)])
    musikgeschmack = StringField("Musikgeschmack", validators=[Length(max=200)])
    wochenend_typ = SelectField(
        "Wochenend-Typ",
        choices=[
            ("", "Keine Angabe"),
            ("ruhig", "Ruhig"),
            ("unterwegs", "Oft unterwegs"),
            ("party", "Party / Ausgang"),
            ("gemischt", "Gemischt"),
        ],
        validators=[Optional()],
    )
    soziales_level = SelectField(
        "WG-Sozialleben",
        choices=[
            ("", "Keine Angabe"),
            ("fuer_mich", "Eher fuer mich"),
            ("gelegentlich", "Gelegentlich zusammen"),
            ("gesellig", "Sehr gesellig"),
        ],
        validators=[Optional()],
    )
    kocht_gern = BooleanField("Kocht gerne")
    bio = TextAreaField("Bio")
    foto = FileField("Bild hochladen (JPEG)", validators=[FileAllowed(["jpg", "jpeg"], "Nur JPEG-Bilder erlaubt.")])
    foto_url = StringField("… oder Bild-URL", validators=[Optional(), URL(message="Bitte eine gültige URL angeben."), Length(max=500)])
    submit = SubmitField("Profil speichern")


class ListingForm(FlaskForm):
    title = StringField("Titel", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Beschreibung", validators=[DataRequired(), Length(max=5000)])
    rent = IntegerField(
        "Miete (CHF)",
        validators=[DataRequired(), NumberRange(min=1, max=100000, message="Bitte eine gültige Miete (1–100000) angeben.")],
    )
    deposit = IntegerField("Depot", validators=[Optional(), NumberRange(min=0, max=100000)])
    kanton = StringField("Kanton", validators=[DataRequired(), Length(max=50)])
    ort = StringField("Ort", validators=[DataRequired(), Length(max=200)])
    strasse = StringField("Strasse", validators=[Optional(), Length(max=200)])
    room_size = IntegerField("Zimmergroesse (m2)", validators=[Optional(), NumberRange(min=1, max=1000)])
    available_from = DateField("Verfuegbar ab", format="%Y-%m-%d", validators=[Optional()])
    furnished = BooleanField("Moebliert")
    pets_allowed = BooleanField("Haustiere erlaubt")
    smoking_allowed = BooleanField("Rauchen erlaubt")
    flatmates = IntegerField("Anzahl Mitbewohner", validators=[Optional(), NumberRange(min=0, max=20)])
    foto = FileField("Bild hochladen (JPEG)", validators=[FileAllowed(["jpg", "jpeg"], "Nur JPEG-Bilder erlaubt.")])
    photo_url = StringField("… oder Bild-URL", validators=[Optional(), URL(message="Bitte eine gültige URL angeben."), Length(max=500)])
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
