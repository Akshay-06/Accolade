from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import psycopg2
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)#os.environ.get('SECRET_KEY')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Log In')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            conn = psycopg2.connect(
                dbname= 'Accolade', #os.environ.get('DB_NAME'),
                user=   'postgres', #os.environ.get('DB_USER'),
                password= 'admin',#os.environ.get('DB_PASSWORD'),
                host=    'localhost', #os.environ.get('DB_HOST'),
                port= '5432'#os.environ.get('DB_PORT')
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM login_details WHERE emp_email=%s AND emp_pass=%s", (form.email.data, form.password.data))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user:
                session['user'] = user[0]
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', form=form, error='Invalid email or password.')
        except Exception as e:
            print(e)
            return render_template('login.html', form=form, error='Unable to log in. Please try again later.')
    else:
        return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user')
    print(user_id)
    if user_id:
        try:
            conn = psycopg2.connect(
                dbname='Accolade', #os.environ.get('DB_NAME'),
                user=   'postgres', #os.environ.get('DB_USER'),
                password= 'admin',#os.environ.get('DB_PASSWORD'),
                host=    'localhost', #os.environ.get('DB_HOST'),
                port= '5432'#os.environ.get('DB_PORT')
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM login_details WHERE id=%s", (user_id,))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user:
                return render_template('dashboard.html', user=user)
            else:
                return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
