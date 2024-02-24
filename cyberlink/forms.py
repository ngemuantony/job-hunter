from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,IntegerField,TextAreaField,FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cyberlink.models import User



# ======================= A class for creating RegisterForms =================================================
class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')

    username = StringField(label="User Name:", validators=[DataRequired(), Length(min=2, max=30)])
    email_address = StringField(label='Email Address:', validators=[DataRequired(), Email()])
    password1 = PasswordField(label='Password:', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(label='Confirm Password:', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Submit')

    def validate_password2(self, password2):
        if self.password1.data != password2.data:
            raise ValidationError('Passwords must match.')


#  ================================= a class Login form and form validations ==================================
class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user is None or not user.check_password(password.data):
            raise ValidationError('Invalid username or password.')
        
# =================================== a class for creating an admin pannel for posting job opportunities =================
class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    salary = IntegerField('Salary')
    currency = StringField('Currency', validators=[DataRequired()])
    responsibilities = TextAreaField('Responsibilities')
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    image = FileField('Image')
