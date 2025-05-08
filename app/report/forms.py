from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class ReportForm(FlaskForm):
    """Base form with common fields"""
    appointment_id = SelectField(
        'Select Appointment',
        coerce=int,
        validators=[DataRequired()],
        choices=[]
    )
    status = SelectField(
        'Status',
        choices=[('inactive', 'Inactive'), ('closed', 'Closed'), ('done', 'Done')]
    )
    submit = SubmitField('Submit Report')

class ClientReportForm(ReportForm):
    """Form for client feedback only"""
    feedback_client = TextAreaField('Client Feedback')

class ProfessionalReportForm(ReportForm):
    """Form for professional feedback only"""
    feedback_professional = TextAreaField('Professional Feedback')