from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user, model_bands

@app.route('/')
def index():
    if 'uuid' not in session:
        return render_template('index.html')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return render_template('index.html')

    session['page'] = 'dashboard'

    context = {
        "user": model_user.User.get_one(session['uuid']),
        "all_bands": model_bands.Band.get_all()
    }

    return render_template('dashboard.html', **context)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'page not found'