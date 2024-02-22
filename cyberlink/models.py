from cyberlink import db


class Job(db.Model):
  id = db.Column(db.Integer, primary_key=True, nullable=False)
  title = db.Column(db.String(50), nullable=False)
  location = db.Column(db.String(50), nullable=False)
  salary = db.Column(db.Integer, nullable=False)
  currency = db.Column(db.String(10), nullable=False)
  responsibilities = db.Column(db.String(2000), nullable=True)
  requirements = db.Column(db.String(2000), nullable=True)
