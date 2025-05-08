from flask_wtf import FlaskForm
from wtforms import DecimalField, EmailField, FileField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TelField
from wtforms.validators import DataRequired, Length, AnyOf, NumberRange, EqualTo, Optional

class ClientRegisterForm(FlaskForm):
    """
        This is the ClientUserForm class that inherits FlaskForm
    """
    email = EmailField('Email',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    retype_password = PasswordField('Retype_password',validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")])
    phone_number  = TelField('Phone_number',validators=[DataRequired()])
    address =  StringField('Address',validators=[DataRequired()])
    age = IntegerField('Age',validators=[
        DataRequired(),
        NumberRange(0,130, message="Age must be between 0 and 130")])

    submit = SubmitField('Sign Up')

class StaffRegisterForm(ClientRegisterForm):
    pay_rate = DecimalField('Payrate',places=2, validators=[DataRequired(),NumberRange(min=0)])
    speciality = StringField('speciality', validators=[DataRequired()])

class LoginForm(FlaskForm):
    """
        This is the LoginForm class that inherits FlaskForm
    """
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sign In')


class ClientProfileForm(FlaskForm):
    """
        This is the ClientUserForm class that inherits FlaskForm
    """
    image = FileField('Image')
    email = EmailField('Email')
    username = StringField('Username')
    password = PasswordField('Password',validators=[DataRequired()])
    phone_number  = TelField('Phone_number')
    address =  StringField('Address')
    age = IntegerField('Age',validators=[
        Optional(),
        NumberRange(0,130, message="Age must be between 0 and 130")])

    submit = SubmitField('Update')

class StaffProfileForm(ClientProfileForm):
    speciality = StringField('speciality', validators=[Optional()])
