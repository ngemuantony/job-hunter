# =========================== Import packages from cyberlink folder which is a package folder  ==============================
# ============================== The classes and objects are mainlly imported from __init__.py which and models.py =============
from cyberlink import app,db,render_template, redirect, url_for, jsonify, request
from cyberlink.models import Job

# ======================== A route for default startup/index page =============================
@app.route('/')
def home_page():
    return render_template('home.html')# Query all jobs from the database

#Display job to the user
# =========================== A route for retrieving jobs from the database and display to the user ===================
@app.route('/job_list')
def job_page():
    all_jobs = Job.query.all()
    return render_template('jobitem.html', jobs=all_jobs)

# ============================= A route for adding and posting jobs to the database ==========================================
# Route to add a new job
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        # Get form data
        title = request.form['title']
        location = request.form['location']
        salary = int(request.form['salary'])
        currency = request.form['currency']
        responsibilities = request.form['responsibilities']
        requirements = request.form['requirements']

        # Create a new job object
        new_job = Job(title=title, location=location, salary=salary, currency=currency, responsibilities=responsibilities, requirements=requirements)

        # Add the new job to the database
        db.session.add(new_job)
        db.session.commit()

        # Redirect to the job list page
        return render_template('job_post.html',messages='Submited succssfully')

    # If GET request, render the form to add a new job
    return render_template('job_post.html')

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
@app.route('/register',methods=['POST','GET'])
def register_page():
    if request.method == 'POST':
        return render_template('register.html')


# ======================== A route for aunthenticating/login user =====================================
@app.route('/login',methods=['POST','GET'])
def login_page():
    if request.method == 'POST':
        return render_template('login.html')
