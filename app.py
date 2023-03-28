from flask import Flask, render_template, request, redirect, session, make_response
from flask_session import Session
import psycopg2

app = Flask(__name__)



# Set up Flask-Session
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_FILE_DIR'] = './.flask_session/'
app.config['SESSION_FILE_THRESHOLD'] = 100
app.config['SESSION_POSTGRES'] = psycopg2.connect(
    host="localhost",
    database="Accolade",
    user="postgres",
    password="admin",
    port=5432
)
Session(app)

# Create user authentication function
def authenticate_user(username, password):
    
    # Set up PostgreSQL connection
    conn = psycopg2.connect(
        host="localhost",
        database="Accolade",
        user="postgres",
        password="admin",
        port=5432
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_details WHERE emp_email=%s AND emp_pass=%s", (username, password))
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
        session['username'] = username
        session['logged_in'] = True
        return redirect('/dashboard')
    else:
        return 'Invalid login credentials'


# Set up dashboard route
@app.route('/dashboard')
def dashboard():
    if 'username' in session and session['logged_in']:
        # Retrieve user data from session
        username = session['username']
        response = make_response(render_template('dashboard.html', username=username))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        # User is not logged in, redirect to login page
        return redirect('/')


@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')


@app.route('/register')
def register():
    return render_template('register.html')

# Set up logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect('/')


if __name__ == '__main__':
  app.run(debug=True)

