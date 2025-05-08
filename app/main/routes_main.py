"""
    This module contains routes for 404 error handeling and
    viewing home, and about html pages in the Flask web application.
"""
from flask import Blueprint, render_template
from . import main
from app.report.report import Report
from models.database import db

def get_db_connection():
    """Helper function to get a database connection"""
    return db.db_conn()

@main.route("/")
def home():
    """
    Method rendering home.html
    """
    conn = get_db_connection()
    reports = Report.get_all(conn)
    testimonials = {report.feedback_client for report in reports if report.feedback_client}
    return render_template('home.html', reviews=testimonials)


@main.errorhandler(404)
def obj_not_found(error):
    """
        Method to handle error case where obj is not found
    """
    return render_template('404.html')
