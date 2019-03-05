from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, IntegerField
from wtforms.validators import Required, Length, Email, Regexp
from ..models import Role, User

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators = [Length(0, 64)])
    location = StringField('Location', validators = [Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators = [Required(), Length(1, 64), Email()])
    username = StringField('Username', validators = [Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, ' 'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce = int)
    name = StringField('Real name', validators = [Length(0, 64)])
    location = StringField('Location', validators = [Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
           User.query.filter_by(email = field.data).first():
            raise ValidationError('Email is already registered')

    def validate_username(self, field):
        if field.data != self.user.username and \
           User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use')

class EditContactForm(FlaskForm):
    first_name = StringField('First Name*', validators = [Length(1, 64)])
    middle_name = StringField('Middle Name')
    last_name = StringField('Last Name*', validators = [Length(1, 64)])
    email = StringField('Email')
    phone_mobile = StringField('Mobile Phone')
    phone_work = StringField('Work Phone')
    phone_home = StringField('Home Phone')
    street_address1 = StringField('Street Address')
    unit_number1 = StringField('Suite/Unit/Apartment Number')
    city1 = StringField('City')
    state1 = StringField('State')
    zip_code1 = StringField('Zip Code')

    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    search = StringField('', render_kw={"placeholder": "Search Contacts"}, )
    submit = SubmitField('Search')

class EditContactFormButton(FlaskForm):
    submit = SubmitField("Edit Contact")

class ButtonAddContactForm(FlaskForm):
    submit = SubmitField("Add Contact")

class AddNoteForm(FlaskForm):
    note = StringField('Note:')
    submit = SubmitField('Add Note')
    
