from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField(
        "სახელი და გვარი",
        validators=[DataRequired(message="სახელი სავალდებულოა"), Length(min=2, max=80)],
    )
    email = StringField(
        "ელ-ფოსტა",
        validators=[DataRequired(message="ელ-ფოსტა სავალდებულოა"), Email(message="ელ-ფოსტა არასწორია")],
    )
    phone = StringField("ტელეფონი (არასავალდებულო)", validators=[Length(max=20)])
    subject = SelectField(
        "თემა",
        choices=[
            ("შეკვეთა", "შეკვეთის გაკეთება"),
            ("ზომა", "ზომასთან დაკავშირებული კითხვა"),
            ("მიტანა", "მიტანის შესახებ"),
            ("სხვა", "სხვა"),
        ],
    )
    message = TextAreaField(
        "შეტყობინება",
        validators=[DataRequired(message="შეტყობინება სავალდებულოა"), Length(min=10, max=2000)],
    )
    submit = SubmitField("გაგზავნა")
