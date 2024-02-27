from flask import render_template, redirect, url_for, jsonify, request, flash
from datetime import datetime
from . import app, db  # Import app and db from the current package
from .models import Job, User, Application, login_manager  # Import login_manager directly
from .forms import RegisterForm, JobForm, LoginForm
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash  # Add this import statement
from flask_login import login_user, login_required, current_user
import os

# Other imports and configurations...

# Import login_manager after initializing app
from .models import login_manager, UserSession, UserPermission

# Imports and configuration for upload functionality...

# Other routes and functions...

# ===================== Imports and configuration for upload functionality =======================
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'cyberlink/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ======================== A route for default startup/index page =================================
@app.route('/')
def home_page():
    print("Rendering home.html")  # Debug print
    return render_template('home.html')  # Query all jobs from the database


# ===================== A route for adding and posting jobs to the database =========================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#=============++++ Route for adding a job with image upload ++++++++++++++++++++++==================
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['image']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully', 'success')
        else:
            flash('Invalid file format. Allowed formats are PNG, JPG, JPEG, and GIF', 'danger')
            return redirect(request.url)
        
        form = JobForm(request.form)
        if form.validate():
            title = form.title.data
            location = form.location.data
            salary = form.salary.data
            currency = form.currency.data
            responsibilities = form.responsibilities.data
            requirements = form.requirements.data

            new_job = Job(title=title, location=location, salary=salary, currency=currency, responsibilities=responsibilities, requirements=requirements, image_address=filename)
            db.session.add(new_job)
            db.session.commit()
            
            flash('Job added successfully', 'success')
            return redirect(url_for('add_job'))
        else:
            flash('Form validation failed. Please check your input.', 'danger')
          return redirect(url_for(home_page))
    
    return render_template('job_post.html', form=JobForm())

# ================================== A route for creating  job API with jsonify the data can be accessed programmatically ====================
# Route to access job data in JSON format
@app.route('/api/jobs')
def jobs():
    jobs = Job.query.all()
    jobs_data = []
    for job in jobs:
        job_data = {
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "salary": job.salary,
            "currency": job.currency,
            "responsibilities": job.responsibilities,
            "requirements": job.requirements
        }
        jobs_data.append(job_data)
    return jsonify(JOBS=jobs_data)

# ======================== A route for registering site users ====================================

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email_address=form.email_address.data).first()
        if existing_user:
            flash('Email address is already registered. Please use a different email address.', 'danger')
            return redirect(url_for('register_page'))
        
        user_to_create = User(username=form.username.data, email_address=form.email_address.data)
        user_to_create.set_password(form.password1.data)
        
        # Set user permissions
        user_to_create.user_permissions = UserPermission.USER  # or UserPermission.ADMIN if applicable
        
        try:
            db.session.add(user_to_create)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login_page'))
        except IntegrityError:
            flash('An error occurred while creating your account. Please try again later.', 'danger')
            db.session.rollback()
    return render_template('register.html', form=form)


# =========================== ADMIN PAGE CUSTOMIZATIONS AND LOGIC =================================
# ========================== A route for administrator dashboard ========================================
@app.route('/admin/dashboard')
def admin_dashboard():
    # Query the database to get the total count of users
    total_users_count = User.query.count()
    print("TOTAL USERS COUNT", total_users_count)
    
    # Query the database to get active users
    active_users = User.query.filter_by(session_state=UserSession.ACTIVE).all()
    
    return render_template('admin_dashboard.html', total_users_count=total_users_count, active_users=active_users)

   

# ======================== A route for retrieving jobs from the database and display to the user====
@app.route('/job_list')
@login_required
def job_page():
    # print("Current user session state:", current_user.session_state)  # Debug print
    # if current_user.session_state == 'ACTIVE':

    all_jobs = Job.query.all()
    print("Rendering jobitem.html")  # Debug print
    return render_template('jobitem.html', jobs=all_jobs)
    # else:
    #     print("Redirecting to login page")  # Debug print
    #     flash('You must be logged in and have an active session to access this page.', 'danger')
    #     return redirect(url_for('login_page'))



# ======================== A route for authenticating/login user ====================================

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username.data
        password = form.password.data

        # Check if the input is an email address
        if '@' in username_or_email:
            user = User.query.filter_by(email_address=username_or_email).first()
        else:
            user = User.query.filter_by(username=username_or_email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Update sign_in_time and session_state
            user.sign_in_time = datetime.now()
            user.session_state = UserSession.ACTIVE  # Set session_state to 'ACTIVE'
            db.session.commit()
            flash('You have been successfully logged in!', 'success')
            
            # Redirect based on user permissions
            if user.user_permissions == UserPermission.ADMIN:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('job_page'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html', form=form)





# Debug prints
print("Routes.py loaded successfully.")
