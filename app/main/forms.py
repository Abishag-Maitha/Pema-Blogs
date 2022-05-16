from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,StringField,ValidationError
from wtforms.validators import DataRequired, Email
from flask_login import current_user
from ..models import User
from flask_wtf.file import FileField,FileAllowed

class UpdateProfile(FlaskForm):
    username = StringField('Enter Your Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    bio = TextAreaField('Write a brief bio about you.',validators = [DataRequired()])
    profile_picture = FileField('profile picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_email(self,email):
        if email.data != current_user.email:
            if User.query.filter_by(email = email.data).first():
                raise ValidationError("That Email has already been taken!")
    
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username = username.data).first():
                raise ValidationError("That username has already been taken")

class Makepost(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = TextAreaField('Blog Content',validators=[DataRequired()])
    submit = SubmitField('Post')

class Comment_Form(FlaskForm):
    content=TextAreaField("comment here", validators=[DataRequired()])
    submit = SubmitField('Submit')