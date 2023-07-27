from flask import *
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from zoneinfo import ZoneInfo
import MySQLdb.cursors
import re
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db=SQLAlchemy(app)

class Mass_ionics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=ZoneInfo('Asia/Kolkata')))

    def __repr__(self):
        return self.title

with app.app_context():
    db.create_all()
    #db.session.commit()

imgfolder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = imgfolder

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Axby20@op00'
app.config['MYSQL_DB'] = 'estatelogin'

mysql = MySQL(app)

@app.route('/')
def mainpg():
    img1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    img2 = os.path.join(app.config['UPLOAD_FOLDER'], 'mainpgimg.jpg')
    return render_template('mainpg.html',user_img=img1, user_img2 = img2)

@app.route('/aboutus')
def aboutus():
    img1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('aboutus.html',user_img=img1)

@app.route('/projects')
def projects():
    img1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('projects.html', user_img=img1)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #Output message if something goes wrong...........
    msg = ''
    #Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Create variables for easy access
        username = request.form['username']
        password = request.form['password']


        #check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))

        #Fetch one record and return result
        account = cursor.fetchone()

        # If account exists in accounts table in our database
        if account:
            # create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            #redirect to home page
            #return 'Logged in successfully!'
            return redirect(url_for('home'))
        else:
            ## Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/login/logout')
def logout():
    # Remove session data, this will log user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    img1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    #Redirect to login page
    return redirect(url_for('projects', user_img=img1))
    #return render_template('login',user_img=img1)


@app.route('/login/register', methods=['GET', 'POST'])
def register():
    #output message if something goes wrong....
    msg=''
    #Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        #Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        #FForm is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message(if any)
    return render_template('register.html', msg = msg)

@app.route('/login/home')
def home():
    #Check if user is loggedin
    if 'loggedin' in session:
        #User is logged in show them the home page
        #return render_template('home.html', username=session['username'])
        return render_template('home.html', username=session['username'])
    #User is not logged in redirect to login page
    return redirect(url_for('login'))

@app.route('/login/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/contactus')
def contactus():
    img1 = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('contactus.html', user_img=img1)

###############--Mass Ionics --####################################################

@app.route('/login/home/mass_ionics')  
def mass_ionics():  
   return render_template('/mass_ionics/mass_ionics.html')

@app.route('/login/home/mass_ionics/mass_ionics_update/', methods=['GET', 'POST'])
def mass_ionics_update():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = Mass_ionics(title=post_title, content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        #return redirect('mass_ionics_update')
        return redirect(url_for('mass_ionics_update'))
    else:
        all_posts=Mass_ionics.query.order_by(Mass_ionics.posted_on).all()
        return render_template('/mass_ionics/mass_ionics_update.html', posts=all_posts)

@app.route('/login/home/mass_ionics/mass_ionics_update/new_post_mass_ionics', methods=['GET', 'POST'])
def new_post_mass_ionics():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = Mass_ionics(title=post_title, content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('mass_ionics_update')
        #return redirect(url_for('mass_ionics_update'))
        #return render_template('/mass_ionics/new_post_mass_ionics.html')
    else:
        return render_template('/mass_ionics/new_post_mass_ionics.html')

@app.route('/login/home/mass_ionics/mass_ionics_update/edit_mass_ionics/<int:id>', methods=['GET', 'POST'])
def edit_mass_ionics(id):
    to_edit = Mass_ionics.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.author = request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        #return redirect('mass_ionics_update')
        return redirect(url_for('mass_ionics_update'))
    else:
        return render_template('/mass_ionics/edit_mass_ionics.html', post=to_edit)

@app.route('/login/home/mass_ionics/mass_ionics_update/delete_mass_ionics/<int:id>')
def delete_mass_ionics(id):
    to_delete = Mass_ionics.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    #return redirect('mass_ionics_update')
    return redirect(url_for('mass_ionics_update'))
    #return render_template('/mass_ionics/new_post_mass_ionics.html')

@app.route('/login/home/massionics/addmassionics', methods=['GET', 'POST'])
def admin():
    #Output message if something goes wrong...........
    msg = ''
    #Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # If account exists in accounts table in our database
        if username == "rupesh" and password == "123456":
            #redirect to Admin
            #return 'Logged in successfully!'
            return render_template('addmassionics.html')
            #return render_template('add.html')
        else:
            ## Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # show the login form with message (if any)
    return render_template('admin.html')


#####################################################
"""


#########################################################


@app.route('/login/home/massionics/addmassionics', methods=['GET', 'POST'])
def admin():
    #Output message if something goes wrong...........
    msg = ''
    #Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #Create variables for easy access
        username = request.form['username']
        password = request.form['password']

        # If account exists in accounts table in our database
        if username == "rupesh" and password == "123456":
            #redirect to Admin
            #return 'Logged in successfully!'
            return render_template('addmassionics.html')
            #return render_template('add.html')
        else:
            ## Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # show the login form with message (if any)
    return render_template('admin.html')



  

@app.route('/login/home/massionics', methods = ['GET', 'POST'])  
def addmassionics():  
    if request.method == 'POST':  
      if not request.form['name']:  
         flash('Please enter all the fields', 'error')  
      else:  
         employee = Employees(request.form['name'])  
           
         db.session.add(employee)  
         db.session.commit()  
         flash('Record was successfully added')  
         return redirect(url_for('listEmployee'))  
    return render_template('addmassionics.html')  

@app.route('/login/home/massionics')  
def delmassionics():  
    employee = request.form['myFunctiondelete']  
    db.session.delete(employee)  
    db.session.commit()  
    flash('Record was successfully deleted')  
    return redirect(url_for('listEmployee'))  

"""
  

if __name__=="__main__":
    app.run(debug=True)

