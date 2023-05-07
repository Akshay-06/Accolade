from datetime import datetime
from flask import Flask, render_template, request, redirect, session, make_response,url_for
from flask_session import Session
from controllers.DBController import connectToDB
from dataclasses import dataclass
from controllers.StackController import main
import os

app = Flask(__name__,static_url_path='', template_folder='views/templates', static_folder='views/static')
rewardpoints = 0

emp_name=''

# Set up Flask-Session
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_FILE_DIR'] = './.flask_session/'
app.config['SESSION_FILE_THRESHOLD'] = 100
app.config['SESSION_POSTGRES'] = connectToDB()
Session(app)

# Create user authentication function
def authenticate_user(username, password):
    global emp_name
    # Set up PostgreSQL connection
    conn = connectToDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_details WHERE emp_email=%s AND emp_pass=%s", (username, password))
    cursor_2 = conn.cursor()
    cursor_2.execute("SELECT emp_name FROM employee where emp_email=%s", (username,))
    name = cursor_2.fetchone()
    emp_name = name[0]
    cursor_2.close()
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

# Set up login page routes
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # Authenticate user
    username = request.form['username']
    password = request.form['password']
    if authenticate_user(username, password):
        
        # Store user data in session
        session['name'] = emp_name
        session['username'] = username
        session['logged_in'] = True
        main()
        return redirect('/home')
    else:
        return render_template('login.html',error='Invalid login credentials')


# Function to register a user
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Get user data from form
        name = request.form['emp_name']
        password = request.form['emp_pwd']
        email = request.form['emp_email']
        stackID = request.form['stack_id']

        # Connect to database
        conn = connectToDB()

        # Create a cursor object
        cur = conn.cursor()

        now = datetime.now()

        # Check if user already exists in database
        cur.execute('SELECT * FROM employee WHERE emp_email = %s', (email,))
        user = cur.fetchone()
        if user:
            error = 'User already exists, please try with other Email ID'
            return render_template('register.html', error=error)
        else:
            # Insert user data into database
            cur.execute('INSERT INTO employee (emp_name, emp_email, stackoverflow_id, created_at, modified_at, created_by, modified_by) VALUES (%s, %s, %s, %s, %s, %s, %s)', (name, email, stackID, now, now, 'admin', 'admin',))
            conn.commit()
            
            cur.execute('SELECT emp_id FROM employee where emp_email= %s',(email,))
            row = cur.fetchone()

            cur.execute('INSERT INTO login_details (emp_id, emp_email, emp_pass, created_at, created_by, modified_at, modified_by) VALUES (%s, %s, %s, %s, %s, %s, %s)', (row[0], email, password, now, 'admin', now, 'admin',)) 
            # Commit changes to database
            conn.commit()
            
            # Close database connection
            cur.close()
            conn.close()
            
            error = 'Registered successfully'
            return render_template('register.html', error=error)
    else:
        return render_template('register.html')
    
@app.route('/registerpage')
def navigateToRegisterPage():
    return render_template('register.html')


@app.route('/sendRewards')
def sendRewards():
    return render_template('rewards.html', error='Form submitted successfully') 


def storeUserInPageAndRedirect(toPage):
    if 'username' in session and session['logged_in']:
        # Retrieve user data from session        
        username = session['username']
        name = session['name']
        response = make_response(render_template(toPage, username=username, name= name)) #name=name
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        # User is not logged in, redirect to login page
        return redirect('/')

# Set up home route
@app.route('/home')
def home():
    return storeUserInPageAndRedirect('home.html')


@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')


# Set up logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.clear()
    return redirect('/')


@app.route('/rewards')
def rewards():
    return storeUserInPageAndRedirect('rewards.html')


@app.route('/profile')
def profile():
    return storeUserInPageAndRedirect('profile.html')

if __name__ == '__main__':
  app.run(debug=True)

