"""
Form for adding a new hair salon appointment, including fields for client selection, 
professional selection, date, time slot and service options.
Validates input with required fields and appropriate constraints.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.user_auth.user_class import User

all_professionals = User.get_professionals()
professionals = [
    (str(p.user_id), p.user_name)  # Ensure this is correctly formatted as a tuple (value, label)
    for p in all_professionals
]

class AppointmentForm(FlaskForm):
    """
    Form for creating and managing salon appointments
    """
    # Client information will typically come from the logged-in user
    # Professional selection
    provider_id = SelectField('Professional', validators=[DataRequired()], choices=professionals)
    
    # Appointment details
    date_appoint = DateField('Appointment Date', validators=[DataRequired()])
    
    slot = SelectField('Time Slot', choices=[
        ('9-10', '9:00-10:00'),
        ('10-11', '10:00-11:00'),
        ('11-12', '11:00-12:00'),
        ('12-13', '12:00-13:00'),
        ('13-14', '13:00-14:00'),
        ('14-15', '14:00-15:00'),
        ('15-16', '15:00-16:00'),
        ('16-17', '16:00-17:00'),
        ('17-18', '17:00-18:00'),
        ('18-19', '18:00-19:00'),
    ], validators=[DataRequired()])
    
    venue = SelectField('Location', choices=[
        ('cmn_room', 'Common Area'),
        ('private', 'Private Room'),
        ('vip_room', 'VIP Suite'),
    ], validators=[DataRequired()])
    
    nber_services = SelectField('Number of Services', choices=[
        (1, '1 service'),
        (2, '2 services'),
        (3, '3 services'),
        (4, '4+ services'),
    ], validators=[DataRequired()], coerce=int)
    
    consumer_report = TextAreaField('Special Request', validators=[Optional(), Length(max=500)])
    
    submit = SubmitField("Book Appointment")

class UpdateAppointmentForm(FlaskForm):
    """
    Form for updating an existing appointment
    """
    
    # Appointment details
    date_appoint = DateField('Appointment Date', validators=[DataRequired()])
    
    slot = SelectField('Time Slot', choices=[
        ('9-10', '9:00-10:00'),
        ('10-11', '10:00-11:00'),
        ('11-12', '11:00-12:00'),
        ('12-13', '12:00-13:00'),
        ('13-14', '13:00-14:00'),
        ('14-15', '14:00-15:00'),
        ('15-16', '15:00-16:00'),
        ('16-17', '16:00-17:00'),
        ('17-18', '17:00-18:00'),
        ('18-19', '18:00-19:00'),
    ], validators=[DataRequired()])
    
    venue = SelectField('Location', choices=[
        ('cmn_room', 'Common Area'),
        ('private', 'Private Room'),
        ('vip_room', 'VIP Suite'),
    ], validators=[DataRequired()])
    
    nber_services = SelectField('Number of Services', choices=[
        (1, '1 service'),
        (2, '2 services'),
        (3, '3 services'),
        (4, '4+ services'),
    ], validators=[DataRequired()], coerce=int)
    
    consumer_report = TextAreaField('Special Request', validators=[Optional(), Length(max=500)])
    
    submit = SubmitField("Update Appointment")