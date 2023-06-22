
from Templates.secret_key import SECRET_KEY
from Templates.sqlalchemy_db_uri import DB_URL
from Templates.database_psw import DB_password
from flask import Flask, render_template, flash, redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField ,SubmitField,DateField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
import bcrypt

from flask_bcrypt import Bcrypt



# Create  a route decorator

# Filters
# safe
# capitalize
# lower
# upper
# title
# trim
# striptags

# Create a secret key for our forms (CRSF)
# We'll create an environemental variable and store it in app.config
# The secret key should not be pushed into gitHub in real developement

# Database with SQLITE
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signIn.db'

# Database with MySQL
# This is done by using app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/db_name'

app = Flask(__name__)

# We'll need to hide here from the public to protect our database password
 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/users'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

# In order to use this we'll need to create a database creating a python file and creating the database, we can then delete the python file once we are done creating the database

# Secret key
app.config['SECRET_KEY'] = SECRET_KEY

# Initializeour database

database = SQLAlchemy(app)
migrate = Migrate(app, database)


# Create Model

class Users(database.Model):
    id =  database.Column( database.Integer, primary_key=True, autoincrement=True)
    Name =  database.Column( database.String(50), nullable=False)
    Surname =  database.Column( database.String(50),nullable=False)
    Email =  database.Column( database.String(120), unique=True, nullable=False)
    password =  database.Column( database.String(128), nullable=False)
    date_signIn = database.Column( database.DateTime, default=datetime.utcnow)

    # Create String to designate 

    def __repr__(self):
        return '<Name %r>' % self.Name
    

    #Check the insert_data() function, the password is rather hashed from there
    

    # def set_password(self, password):
    #     self.password = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password, password)
      
# Define a form class

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),EqualTo('conf_password', message='Passwords Must Match.')])
    conf_password = PasswordField('Confirm Password', validators=[DataRequired()])
    birthdate = DateField('Birthdate', format='%Y-%m-%d',validators=[DataRequired()])
    submit = SubmitField('Submit')
    
    



garden =['Tomatoes', 'Yam', 'Orange', 'Apple']

not_fruit = "<h1>Not a fruit</h1>"





@app.route("/check")

def index():
    return render_template("preloader.html")

@app.route("/about")
def about():
    
    return render_template("about.html")

# Example: localhost5000/user/Bob

@app.route("/user/<name>/<surname>")
def user(name,surname):
    return render_template("welcom_msg.html", name=name, surname=surname)

@app.route("/users")
def view_user():

    num_rows = Users.query.count()

    database = pymysql.connect(host='localhost', user='root',password=DB_password) 
    #Create a cursor object to execute SQL queries
    cursor = database.cursor()

    sql= 'SELECT * FROM users.users'

    # Execute the query
    cursor.execute(sql)

    # Fetch all rows returned by the query
    data = cursor.fetchall()

    database.commit()
    
    database.close()

    # Pass the data to the template for rendering
    return render_template('userlist.html', data=data, num_rows=num_rows)
 


    

# Sign In route and function
@app.route("/")
def Home():
    return render_template("preloader.html")

@app.route("/SignIn", methods=['GET', 'POST'])
def Sign_In():
    name = None
    form = UserForm()
    

    # Here we'll validate Form
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        birthdate = form.birthdate.data
        password = form.password.data
        
        insert_data(name, surname, email,  birthdate,password)


        # form.name.data = ''
        # form.surname.data = ''
        # form.email.data = ''
        # form.birthdate.data = ''
        # form.password.data = ''

        flash("Your Form has been submitted successfully!")

    # our_users= Users.query.order_by(Users.date_signIn)
    return render_template("user_signIn.html", name=name,form=form)


# Insert Data into MySQL

def insert_data(name,surname,email,birthdate,password):

    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    
    date = datetime.utcnow()

    conn = pymysql.connect(host='localhost', user='root', password=DB_password)
    cursor = conn.cursor()
    query = "INSERT INTO users.users (Name,Surname, Email,birthdate, password, date_signIn) VALUES (%s, %s, %s, %s, %s,%s)"
    values = (name,surname,email,birthdate,hashed_password,date)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()



# Create custom error pages

# Invalid URL
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

# Inernal Server Error
@app.errorhandler(500)
def page_not_found(error):
    return render_template("500.html"), 500



@app.route('/delete/<int:id>')
def delete_item(id):
    user_to_delete = Users.query.get_or_404(id)  # Retrieve the item from the database
    # name = None
    form = UserForm()
    Name = form.name.data
    try:
        name = form.name.data
        database.session.delete(user_to_delete)  # Delete the item from the database
        database.session.commit()
        flash('User Deleted successfully!!')
        
        our_users= Users.query.order_by(Users.date_signIn)
        
        return render_template("delmsg.html", Name=Name,form=form,our_users=our_users, id=id)
        

    except:

        flash('There was a problem deleting User, Try again.')   
        return render_template("delmsg.html", Name=Name,form=form,our_users=our_users) 

    


if __name__ == '__main__':

    with app.app_context():
        database.create_all()

    app.run(debug=True)  
    
  