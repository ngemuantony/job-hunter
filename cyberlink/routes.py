# =========================== Import packages from cyberlink folder which is a package folder  ==============================
# ============================== The classes and objects are mainlly imported from __init__.py which and models.py =============
from cyberlink import app,db
from flask import render_template, redirect, url_for, jsonify, request,flash, redirect,url_for
from cyberlink.models import Job,User,Application
from cyberlink.forms import RegisterForm,JobForm
from sqlalchemy.exc import IntegrityError
import os


# ===================== Imports and configuration for upload functionality =======================
from werkzeug.utils import secure_filename
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'cyberlink/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ======================== A route for default startup/index page =================================
@app.route('/')
def home_page():
    return render_template('home.html')# Query all jobs from the database
   
#Display job to the user
# ======================== A route for retrieving jobs from the database and display to the user====
@app.route('/job_list')
def job_page():
    all_jobs = Job.query.all()
    return render_template('jobitem.html', jobs=all_jobs)

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
            return redirect(url_for('job_page'))
        else:
            flash('Form validation failed. Please check your input.', 'danger')
    
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
        
        try:
            db.session.add(user_to_create)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login_page'))
        except IntegrityError:
            flash('An error occurred while creating your account. Please try again later.', 'danger')
            db.session.rollback()
    return render_template('register.html', form=form)


# ======================== A route for aunthenticating/login user =====================================
@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        # Logic for handling login form submission
        # Assuming you'll authenticate the user here
        flash('You have been successfully logged in!', 'success')
        return redirect(url_for('home_page'))
    return render_template('login.html')
    