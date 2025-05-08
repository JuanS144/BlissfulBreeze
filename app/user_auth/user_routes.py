from flask import current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from . import user_auth
from .user_forms import ClientRegisterForm, StaffRegisterForm,LoginForm, ClientProfileForm, StaffProfileForm
from .user_class import User
from werkzeug.utils import secure_filename
import os
import time
import random
import string

@user_auth.route('/register', methods=['GET','POST'])
def register():
    """
        Method rendering register.html, and redirecting
        to login.html upon sucessful registeration
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
        return redirect(url_for('user_auth.login'))
    
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
        return redirect(url_for('user_auth.login'))
    
    return render_template('register.html', client_form=client_form, staff_form=staff_form)
@user_auth.route('/login', methods=['GET','POST'])
def login():
    """
        Method rendering login.html and redirecting
        to profile in case of successful login.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            user.activate_user()
            login_user(user)
            flash("Login Success!",'success')
            return redirect(url_for('user_auth.profile'))
        else:
            flash("User not found ! Verify your username / password.",'fail')
    return render_template('login.html', form=form)

@login_required
@user_auth.route('/logout')
def logout():
    """
        User logout view.
    """
    current_user.deactivate_user()
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

@login_required
@user_auth.route('/profile',methods=['GET','POST'])
def profile():
    
    if current_user.user_type == "client":
        form=ClientProfileForm()
    else:
        form=StaffProfileForm()


    if form.validate_on_submit():
        if form.email.data:
            current_user.email = form.email.data
        if form.username.data:
            current_user.user_name = form.username.data
        if form.phone_number.data:
            current_user.phone_number = form.phone_number.data
        if form.address.data:
            current_user.address = form.address.data
        if form.image.data and User.allowed_file(form.image.data.filename):
            current_user.user_image = upload_image(form.image.data)

        speciality = getattr(form, 'speciality', None)

        if current_user.check_password(form.password.data):
            current_user.update_user()
            if speciality and speciality.data:
                current_user.speciality = speciality.data
                current_user.update_speciality()
            flash("Success! Profile updated.")
        else:
            flash("Wrong Password!! Please input correct password to update profile.")
    return render_template('profile.html', form=form)

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