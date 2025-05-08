"""
Define the routes for administration BP
"""

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

from app.main.routes_main import obj_not_found
from . import admin
from app.admin.admin_forms import AdminRegisterForm, ClientRegisterForm, StaffRegisterForm, ClientProfileForm, AdminProfileForm, StaffProfileForm
from app.admin.admin_class import User
from werkzeug.utils import secure_filename
import os
import time
import random
import string

@admin.route('/members', methods=['GET','POST'])
@login_required
def members():
    """
    Lists members to administrate.
    """
    client_form =  ClientRegisterForm()
    staff_form = StaffRegisterForm()

    if client_form.validate_on_submit():
        User.add_user(
            user_name=client_form.username.data,
            email=client_form.email.data,
            password=client_form.password.data,
            phone_number=client_form.phone_number.data,
            address=client_form.address.data,
            age=client_form.age.data
        )


        flash("Register successful!",'success')
    
    if staff_form.validate_on_submit():
        User.add_user(
            username=staff_form.username.data,
            email=staff_form.email.data,
            password=staff_form.password.data,
            phone_number=staff_form.phone_number.data,
            address=staff_form.address.data,
            age=staff_form.age.data,
            pay_rate=staff_form.pay_rate.data,
            speciality=staff_form.speciality.data,
            user_type='Professional'
        )
        flash("Register successful!",'success')
    
    return render_template('members.html', client_form=client_form, staff_form=staff_form, members=User.get_members())

@admin.route('/admins', methods=['GET', 'POST'])
@login_required
def admins():
    """
    Lists admins to administrate.
    """
    form = AdminRegisterForm()

    if form.validate_on_submit():
        User.add_user(
            user_name=form.username.data,
            email=form.email.data,
            password=form.password.data,
            phone_number=form.phone_number.data,
            address=form.address.data,
            age=form.age.data,
            pay_rate=form.pay_rate.data,
            user_type="admin",
            access_level=form.access_level.data
        )

        flash("Register successful!",'success')
        return render_template('admins.html', admins=User.get_admins(), form=form)

    return render_template('admins.html', admins=User.get_admins(), form=form)

@admin.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.user_type != "admin":
        return obj_not_found(404)

    user = User.get_user_by_id(user_id)
    if user.user_type == "admin":
        form=AdminProfileForm()
        if request.method == "GET":
            form.access_level.data = int(user.access_level)
    elif user.user_type == "professional":
        form=StaffProfileForm()
    else:
        form=ClientProfileForm()


    if form.validate_on_submit():
        if form.email.data:
            user.email = form.email.data
        if form.username.data:
            user.user_name = form.username.data
        if form.phone_number.data:
            user.phone_number = form.phone_number.data
        if form.address.data:
            user.address = form.address.data
        if form.image.data:
            user.user_image = upload_image(form.image.data)
        if form.age.data:
            user.age = form.age.data


        pay_rate = getattr(form, 'pay_rate', None)
        access_level = getattr(form, 'access_level', None)
        speciality = getattr(form, 'speciality', None)


        if current_user.check_password(form.password.data):
            user.update_user()
            
            if pay_rate and pay_rate.data is not None:
                user.pay_rate = pay_rate.data
                user.update_pay_rate()
            if speciality and speciality.data:
                user.speciality = speciality.data
                user.update_speciality()
            if access_level:
                user.access_level = access_level.data
                user.update_admin()

            
            flash("Success! Profile updated.")
        else:
            flash("Wrong Password!! Please input correct password to update profile.")
    return render_template('edit_user.html', given_user=user, form=form)

@admin.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # Only allow admins to delete users
    if current_user.user_type != "admin":
        flash("You do not have permission to delete users.", "danger")
        return redirect(request.referrer or url_for('admin.members'))  # Redirect to the users list page (adjust this as needed)

    # Get the user by id
    user = User.get_user_by_id(user_id)
    
    if not user:
        flash(f"User with ID {user_id} not found.", "danger")
        return redirect(url_for('admin.members'))  # Redirect to users list

    try:
        # Here, you can check if the user is an admin or if there are other conditions before deleting.
        User.delete_user(user_id)  # Call the method to delete the user

        flash(f"User {user.user_name} has been deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "danger")
    if user.access_level == 1:
        return redirect(url_for('admin.members'))  # Redirect to users list
    return redirect(url_for('admin.admins'))  # Redirect to users list

def generate_unique_filename(original_filename):
    # Get the file extension
    file_extension = os.path.splitext(original_filename)[1]
    
    # Generate a unique string based on timestamp and random string
    unique_str = str(int(time.time())) + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # Create the final filename
    unique_filename = f"{unique_str}{file_extension}"
    return unique_filename

# Function to handle the file upload
def upload_image(form_image):
        # Secure the filename to prevent directory traversal
        filename = secure_filename(form_image.filename)
        
        # Generate a unique filename
        unique_filename = generate_unique_filename(filename)
        
        # Define the upload folder (you can change this path)
        upload_folder = os.path.join(current_app.root_path,'static', 'images', 'profiles')
        
        # Save the file to the server
        file_path = os.path.join(upload_folder, unique_filename)
        form_image.save(file_path)

        return unique_filename
