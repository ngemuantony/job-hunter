from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [{
    "id":
    1,
    "title":
    "Data Scientist",
    "location":
    "Nairobi, Kenya",
    "company":
    "Google",
    "salary":
    "Ksh 230,000",
    "description":
    "Join Google's dynamic team as a Data Scientist and unlock the power of data to drive insights and innovation. Utilize your analytical skills to extract valuable information from large datasets, develop predictive models, and drive data-driven decision-making processes. Collaborate with cross-functional teams to solve complex problems and make a meaningful impact on the world."
}, {
    "id":
    2,
    "title":
    "Frontend Engineer",
    "location":
    "Nairobi, Kenya",
    "company":
    "Microsoft",
    "salary":
    "Ksh 210,000",
    "description":
    "As a Frontend Engineer at Microsoft, you'll be at the forefront of creating user-friendly and visually appealing web interfaces. Collaborate with designers and backend developers to implement responsive and interactive designs. Leverage your expertise in HTML, CSS, and JavaScript to deliver seamless user experiences across multiple devices and platforms."
}, {
    "id":
    3,
    "title":
    "Backend Engineer",
    "location":
    "Nairobi, Kenya",
    "company":
    "Amazon",
    "salary":
    "Ksh 220,000",
    "description":
    "Join Amazon's backend engineering team and play a key role in building scalable and reliable systems to power the world's largest online marketplace. Design and develop robust backend services and APIs that handle millions of requests per day. Work with cutting-edge technologies to optimize performance, improve scalability, and ensure the security of our systems."
}, {
    "id":
    4,
    "title":
    "Cyber Security Analyst",
    "location":
    "Mombasa, Kenya",
    "company":
    "Naivas",
    "salary":
    "Ksh 180,000",
    "description":
    "Protect Naivas' digital assets from cyber threats as a Cyber Security Analyst. Monitor and analyze security incidents, conduct vulnerability assessments, and implement security controls to safeguard the organization's information systems. Stay ahead of emerging threats and trends in the cybersecurity landscape to ensure Naivas remains secure and resilient."
}, {
    "id":
    5,
    "title":
    "Ethical Hacker",
    "location":
    "Kisumu, Kenya",
    "company":
    "CBK",
    "salary":
    "Ksh 200,000",
    "description":
    "Join the Central Bank of Kenya as an Ethical Hacker and utilize your skills to identify and mitigate potential security vulnerabilities. Conduct penetration testing, ethical hacking, and security assessments to proactively identify weaknesses in CBK's systems and applications. Collaborate with stakeholders to develop and implement effective security measures to protect sensitive information and maintain regulatory compliance."
}, {
    "id":
    6,
    "title":
    "Network Engineer",
    "location":
    "Machakos, Kenya",
    "company":
    "Google",
    "salary":
    "Ksh 210,000",
    "description":
    "Be part of Google's network engineering team and help build and maintain the backbone of the internet. Design, deploy, and optimize scalable network infrastructures to support Google's vast array of products and services. Collaborate with cross-functional teams to troubleshoot network issues, optimize performance, and ensure the reliability and security of Google's global network."
}, {
    "id":
    7,
    "title":
    "System Analyst",
    "location":
    "Nairobi, Kenya",
    "company":
    "Microsoft",
    "salary":
    "Ksh 200,000",
    "description":
    "Join Microsoft as a System Analyst and play a crucial role in optimizing and enhancing the organization's IT systems and processes. Analyze user requirements, design system solutions, and oversee the implementation and integration of new technologies. Collaborate with stakeholders to streamline workflows, improve efficiency, and drive innovation across Microsoft's diverse range of products and services."
}, {
    "id":
    8,
    "title":
    "Database Administrator",
    "location":
    "Nairobi, Kenya",
    "company":
    "Amazon",
    "salary":
    "Ksh 220,000",
    "description":
    "Manage and optimize Amazon's vast databases as a Database Administrator. Ensure the reliability, performance, and security of Amazon's data infrastructure by implementing effective backup and recovery strategies, monitoring database performance, and implementing security best practices. Collaborate with development teams to design and optimize database schemas and queries, enabling Amazon to deliver seamless customer experiences."
}]


@app.route('/')
def home_page():
  return render_template('home.html', jobs=JOBS)


# Creating an endpoint to access data for other programmers to work with.
@app.route('/api/jobs')
def jobs():
  # Extracting data through (Javascript Object) jsonify
  return jsonify(JOBS)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
