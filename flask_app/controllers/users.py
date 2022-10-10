from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User # this imports the User class from the users.py file inside the models folder
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/') # default route
def index():
    return render_template('index.html')

@app.route('/create_user', methods=['POST'])
def register():
    if not User.validate_create(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.create_user(data)
    session['user_id'] = user_id
    return render_template('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid email/password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email/password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return render_template('welcome.html', user=user_in_db)