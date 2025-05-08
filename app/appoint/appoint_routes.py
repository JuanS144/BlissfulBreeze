"""
Define the routes for appointments (list all appointments) and appointment (show one appointment).
"""

from flask import render_template, flash, url_for, redirect, session, request
from flask_login import login_user, logout_user, login_required, current_user
from .appoint_class import Appointment
from .appoint_forms import AppointmentForm, UpdateAppointmentForm
from app.main.routes_main import obj_not_found

from app.user_auth.user_class import User

from . import appoint

@appoint.route('/appointments', methods=['GET'])
@login_required
def list_appointments():
    """
    List all appointments based on the user's role.
    Admin_Appoint can see all appointments, others can see only theirs.
    """

    appointments = Appointment.get_appointments(current_user.user_id, current_user.access_level)
    return render_template('appointments.html', appointments=appointments)


@appoint.route('/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """
    Show a specific appointment based on the appointment_id.
    """
    appointment_item = Appointment.get_appointment(appointment_id)
    if appointment_item is None:
        return obj_not_found(404)
    return render_template('appointment.html', appointment=appointment_item)


@appoint.route('/new_appointment', methods=['GET', 'POST'])
@login_required
def new_appointment():
    """
    Create a new appointment.
    """
    form = AppointmentForm()
    form.submit.label.text = "Book Appointment"

    if form.validate_on_submit():
        # Create new appointment from form data
        new_appt = Appointment(
            appointment_id=None,
            consumer_id=current_user.user_id,
            provider_id=form.provider_id.data,
            consumer_name=current_user.user_name,
            provider_name=User.get_username_from_id(form.provider_id.data),
            date_appoint=form.date_appoint.data,
            slot=form.slot.data,
            venue=form.venue.data,
            nber_services=form.nber_services.data,
            consumer_report=form.consumer_report.data,
        )
        
        # Add the appointment to the database
        appointment_id = Appointment.add_appointment(new_appt)
        
        if appointment_id:
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('appoint.get_appointment', appointment_id=appointment_id))
        else:
            flash('Failed to book appointment. Please try again.', 'error')
    
    return render_template('new_appointment.html', form=form)


@appoint.route('/appointments/<int:appointment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_appointment(appointment_id):
    """
    Edit an existing appointment.
    """
    appointment = Appointment.get_appointment(appointment_id)
    
    if appointment is None:
        return obj_not_found(404)
    
    # Check if current user owns this appointment or is admin
    if current_user.user_id != appointment.consumer_id and current_user.access_level != 2 and current_user.access_level != 4:
        flash("You don't have permission to edit this appointment", 'error')
        return redirect(url_for('appoint.get_appointment', appointment_id=appointment_id))
    
    form = UpdateAppointmentForm()
    form.submit.label.text = "Update Appointment"

    # Populate form with current appointment values on GET
    if request.method == 'GET':
        flash('Note: You must cancel this appointment and make a new one to change professionals.', 'info')
        form.date_appoint.data = appointment.date_appoint
        form.slot.data = appointment.slot
        form.venue.data = appointment.venue
        form.nber_services.data = appointment.nber_services
        form.consumer_report.data = appointment.consumer_report

    # Process the form submission
    if form.validate_on_submit():
        success = Appointment.update_appointment(
            appointment_id,
            date_appoint=form.date_appoint.data,
            slot=form.slot.data,
            venue=form.venue.data,
            nber_services=form.nber_services.data,
            consumer_report=form.consumer_report.data
        )
        

        if success:
            flash('Appointment updated successfully!', 'success')
            return redirect(url_for('appoint.get_appointment', appointment_id=appointment_id))
        else:
            flash('Failed to update appointment. Please try again.', 'error')
    
    return render_template('edit_appointment.html', form=form, appointment=appointment)


@appoint.route('/cancel/<int:appointment_id>', methods=['POST','GET'])
@login_required
def cancel_appointment(appointment_id):
    """
    Cancel an existing appointment.
    """
    # Get the appointment by id
    appointment = Appointment.get_appointment(appointment_id)
    
    if not appointment:
        flash(f"Appointment with ID {appointment_id} not found.", "danger")
        return redirect(url_for('appoint.list_appointments'))  # Redirect to appointment list

    try:
        # Here, you can check if the user is an admin or if there are other conditions before deleting.
        Appointment.cancel_appointment(appointment_id)  # Call the method to delete the user

        flash(f"Appointment of {appointment.consumer_name} with {appointment.provider_name} has been deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "danger")
    return redirect(url_for('appoint.list_appointments'))  # Redirect to appointment list