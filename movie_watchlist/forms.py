from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, URLField, HiddenField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, EqualTo
from datetime import date

todays_date = date.today()


class StringListField(HiddenField):
    def _value(self):
        if self.data:
            return (",").join(self.data)
        return ""

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [x.strip().capitalize() for x in valuelist[0].split(",")]
        else:
            self.data = []

class CapitalizeTextField(StringField):
    def process_formdata(self, value):
        capitalized_data = [x.capitalize() for x in value[0].split(" ")]
        self.data = (" ").join(capitalized_data)

class AddMovie(FlaskForm):
    title = CapitalizeTextField("Title", validators=[DataRequired()])
    director = CapitalizeTextField(
        "Director", validators=[DataRequired(message="Field must be at least 3 characters long."), Length(min=3)]
    )
    year = IntegerField(
        "Year",
        validators=[
            DataRequired(message="Year must be greater than or equal 1878."),
            NumberRange(min=1878, message="Year must be greater than or equal 1878."),
        ],
    )

class UpdateMovie(AddMovie):
    casts = StringListField("Casts (enter a cast and click button to add)")
    series = StringListField("Series (enter a series and click button to add)")
    tags = StringListField("Tags (enter a tag and click button to add)")
    description = TextAreaField("Description")
    video = URLField(
        "Video link",
        validators=[
            Regexp(
                r"^$|^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$",
                message="Video link must be a valid url.",
            )
        ],
    )

class LogIn(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email field is required."),
            Regexp(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", message="Please enter a valid email."),
        ],
    )
    password = PasswordField("Password", [DataRequired(message="Password is required."),])

class RegisterUser(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired(message="Email field is required"),
            Regexp(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", message="Please enter a valid email"),
        ],
    )
    password = PasswordField("Password", [DataRequired(message="Password is required."), Length(min=5, message="Password must be at least 5 characters long."), EqualTo("confirm", message="Passwords must match.")])
    confirm = PasswordField("Confirm Password")
