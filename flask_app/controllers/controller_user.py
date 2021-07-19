from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/login')
def login():
    session['page'] = 'login'
    return render_template('index.html')

@app.route('/register')
def register():
    session['page'] = 'register'
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/user/create', methods=['post'])
def create_user():
    is_valid = model_user.User.validate_user(request.form)

    if not is_valid:
        return redirect('/register')

    hash_pw = bcrypt.generate_password_hash(request.form['pw'])

    info = {
        **request.form,
        "hash_pw": hash_pw
    }
    user_id = model_user.User.create(info)
    session['uuid'] = user_id
    return redirect('/')

@app.route('/process_login', methods=['POST'])
def process_login():
    user_list = model_user.User.get_one_by_email(request.form['email'])

    if len(user_list) == 0:
        flash('User not found')
        return redirect('/')

    user = user_list[0]

    if not bcrypt.check_password_hash(user['hash_pw'], request.form['pw']):
        flash("Invalid Credentials")
        return redirect('/')
    
    session['uuid'] = user['id']
    return redirect('/')

@app.route('/user/<int:id>')
def show_user(id):
    return 'show user'

@app.route('/user/<int:id>/edit')
def edit_user(id):
    return 'edit user'

@app.route('/user/<int:id>/update', methods=['post'])
def update_user(id):
    return 'update user'

@app.route('/user/<int:id>/delete')
def delete_user(id):
    return 'delete user'