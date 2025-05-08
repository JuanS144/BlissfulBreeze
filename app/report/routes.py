from flask import Blueprint, render_template, request, redirect, url_for, flash
from .report import Report
import psycopg2
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from .forms import ReportForm, ClientReportForm, ProfessionalReportForm
from models.database import db
from . import report_bp

# ---- Routes ----

def get_db_connection():
    """Helper function to get a database connection"""
    return db.db_conn()
def is_admin(user):
    """Helper function to check if user has admin privileges"""
    return int(user.access_level) in [2, 4]  # 2 for admin_appoint, 4 for admin_super

@report_bp.route('/')
@login_required
def list_reports():
    conn = None
    try:
    
        print("User ID:", current_user.user_id)
        print("Access Level:", current_user.access_level)
        conn = get_db_connection()

        if is_admin(current_user):
            # Admins can see all reports
            reports = Report.get_all(conn)
        else:
            # Get reports for the current user's appointments
            reports = []
            all_reports = Report.get_all(conn)
            for report in all_reports:
                if Report.validate_appointment_ownership(conn, report.appointment_id, current_user.user_id):
                    reports.append(report)

        return render_template('list.html', reports=reports)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return render_template('list.html', reports=[])
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass


@report_bp.route('/<int:report_id>')
@login_required
def view_report(report_id):
    conn = None
    try:
        conn = get_db_connection()
        report = Report.get_by_id(conn, report_id)
        if not report:
            flash("Report not found", "danger")
            return redirect(url_for('report_bp.list_reports'))
            
        # Check if user has permission to view this report
        if not is_admin(current_user) and not Report.validate_appointment_ownership(conn, report.appointment_id, current_user.user_id):
            flash("You don't have permission to view this report", "danger")
            return redirect(url_for('report_bp.list_reports'))
            
        return render_template('view.html', report=report)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('report_bp.list_reports'))
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

def get_user_id():
    """Helper function to get user ID from either JWT or session"""
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except:
        return current_user.user_id if current_user.is_authenticated else None

@report_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_report():
    # Determine if user is client or professional based on appointment
    conn = None
    try:
        conn = get_db_connection()
        appointments = Report.get_available_appointments(
            conn, 
            user_id=current_user.user_id,
            is_admin=is_admin(current_user)
        )
        
        # Choose form based on user role in appointment
        is_professional = False
        if appointments:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT provider_id FROM salon_appointment 
                    WHERE appointment_id = %s
                """, (appointments[0][0],))
                provider_id = cur.fetchone()[0]
                is_professional = (provider_id == current_user.user_id)

        form = ProfessionalReportForm() if is_professional else ClientReportForm()
        form.appointment_id.choices = [(id, label) for id, label in appointments]

        if form.validate_on_submit():
            existing_report = Report.get_by_appointment_id(conn, form.appointment_id.data)
            
            if existing_report:
                # Update existing report with the appropriate feedback
                if is_professional:
                    existing_report.feedback_professional = form.feedback_professional.data
                else:
                    existing_report.feedback_client = form.feedback_client.data
                Report.update(conn, existing_report)
                flash('Feedback added successfully.', 'success')
            else:
                # Create new report
                new_report = Report(
                    report_id=None,
                    appointment_id=form.appointment_id.data,
                    status=form.status.data,
                    feedback_client=form.feedback_client.data if not is_professional else None,
                    feedback_professional=form.feedback_professional.data if is_professional else None
                )
                report_id = Report.create(conn, new_report)
                flash('Report created successfully.', 'success')
                return redirect(url_for('report_bp.view_report', report_id=report_id))

        reports = Report.get_user_reports(conn, current_user.user_id)
        return render_template('create.html', form=form, reports=reports, is_professional=is_professional)

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return render_template('create.html', form=form, reports=[])
    finally:
        if conn:
            conn.close()


@report_bp.route('/edit/<int:report_id>', methods=['GET', 'POST'])
@login_required
def edit_report(report_id):
    conn = None
    try:
        conn = get_db_connection()
        report = Report.get_by_id(conn, report_id)

        if not report:
            flash("Report not found", "danger")
            return redirect(url_for('report_bp.list_reports'))

        # Check permissions
        if not is_admin(current_user) and not Report.validate_appointment_ownership(conn, report.appointment_id, current_user.user_id):
            flash("You don't have permission to edit this report", "danger")
            return redirect(url_for('report_bp.list_reports'))

        # Determine if user is professional
        with conn.cursor() as cur:
            cur.execute("""
                SELECT provider_id FROM salon_appointment 
                WHERE appointment_id = %s
            """, (report.appointment_id,))
            provider_id = cur.fetchone()[0]
            is_professional = (provider_id == current_user.user_id)

        # Create form based on role
        form = ProfessionalReportForm() if is_professional else ClientReportForm()
        
        # Get all available appointments for the user
        appointments = Report.get_available_appointments(
            conn, 
            user_id=current_user.user_id,
            is_admin=is_admin(current_user)
        )
        
        # Add current appointment to choices if not in list
        current_appointment = None
        with conn.cursor() as cur:
            cur.execute("""
                SELECT appointment_id, 
                       CONCAT('Appointment #', appointment_id, ' - ', consumer_name, ' with ', provider_name)
                FROM salon_appointment 
                WHERE appointment_id = %s
            """, (report.appointment_id,))
            current_appointment = cur.fetchone()
        
        all_choices = [current_appointment] + appointments if current_appointment not in appointments else appointments
        form.appointment_id.choices = [(id, label) for id, label in all_choices]

        if request.method == 'GET':
            form.appointment_id.data = report.appointment_id
            form.status.data = report.status
            if is_professional:
                form.feedback_professional.data = report.feedback_professional
            else:
                form.feedback_client.data = report.feedback_client

        if form.validate_on_submit():
            report.appointment_id = form.appointment_id.data
            report.status = form.status.data
            if is_professional:
                report.feedback_professional = form.feedback_professional.data
            else:
                report.feedback_client = form.feedback_client.data

            Report.update(conn, report)
            flash("Report updated successfully.", "success")
            return redirect(url_for('report_bp.view_report', report_id=report.report_id))

        return render_template('edit.html', form=form, report_id=report_id, is_professional=is_professional)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('report_bp.list_reports'))
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

@report_bp.route('/delete/<int:report_id>', methods=['POST'])
@login_required
def delete_report(report_id):
    conn = None
    try:
        conn = get_db_connection()
        report = Report.get_by_id(conn, report_id)

        if not report:
            flash("Report not found", "danger")
            return redirect(url_for('report_bp.list_reports'))

         # Check permissions - admins can delete all reports
        if not is_admin(current_user) and not Report.validate_appointment_ownership(conn, report.appointment_id, current_user.user_id):
            flash("You don't have permission to delete this report", "danger")
            return redirect(request.referrer or url_for('report_bp.list_reports'))

        Report.delete(conn, report_id)
        flash("Report deleted.", "warning")
        return redirect(request.referrer or url_for('report_bp.list_reports'))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(request.referrer or url_for('report_bp.list_reports'))
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass
