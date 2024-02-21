from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Construct the database URI
db_uri = 'postgresql://postgres.ucxjsekrjjmujvckekuq:Juliet$$2006##@aws-0-us-west-1.pooler.supabase.com:5432/postgres'

# Set the database URI in the Flask app configuration
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # For automatically creating tables

db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    responsibilities = db.Column(db.String(2000), nullable=True)
    requirements = db.Column(db.String(2000), nullable=True)

with app.app_context():
    db.create_all()

# Route to render the home page with all jobs
@app.route('/')
def home_page():
    # Query all jobs from the database
    all_jobs = Job.query.all()
    return render_template('jobitem.html', jobs="all_jobs")


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
        return redirect(url_for('home_page'))

    # If GET request, render the form to add a new job
    return render_template('jobs.html')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
