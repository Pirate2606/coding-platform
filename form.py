from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class Feedback(FlaskForm):

    email = StringField(validators = [DataRequired(), Email('* Enter valid email id')])
    message = TextAreaField(validators = [DataRequired()])
    submit = SubmitField('Submit')
