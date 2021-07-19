from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models import model_user, model_bands

@app.route('/band/new')
def new_band():
    session['page']= 'new_band'
    context = {
        "user": model_user.User.get_one(session['uuid'])
    }
    return render_template('band_new.html', **context)

@app.route('/band/create', methods=['post'])
def create_band():
    is_valid = model_bands.Band.validate_bands(request.form)

    if not is_valid:
        return redirect('/band/new')

    info = {
        **request.form,
        "creator_id": session['uuid']
    }
    model_bands.Band.create(info)

    return redirect('/')

@app.route('/band/<int:band_id>/join')
def join_band(band_id):
    info = {
        "user_id": session['uuid'],
        "band_id": band_id
    }
    model_bands.Band.join_one(info)
    return redirect('/')

@app.route('/band/<int:band_id>/quit')
def leave_band(band_id):
    info = {
        "user_id": session['uuid'],
        "band_id": band_id
    }
    model_bands.Band.leave_one(info)
    return redirect('/')

@app.route('/band/<int:user_id>/all')
def show_band(user_id):
    context = {
        "user": model_user.User.get_one(session['uuid'])
    }
    return render_template('bands_mine.html', **context)

# @app.route('/band/<int:id>')
# def show_band(id):
#     context = {
#         "user": model_user.User.get_one(session['uuid'])
#     }
#     return render_template('band_show.html', **context)

@app.route('/band/<int:id>/edit')
def edit_band(id):
    context = {
        "user": model_user.User.get_one(session['uuid']),
        "band": model_bands.Band.get_one(id)
    }
    return render_template('band_edit.html', **context)

@app.route('/band/<int:id>/update', methods=['post'])
def update_band(id):
    is_valid = model_bands.Band.validate_bands(request.form)

    if not is_valid:
        return redirect(f'/band/{id}/edit')
    
    info = {
        **request.form,
        "band_id": id
    }
    model_bands.Band.update_one(info)
    return redirect('/')

@app.route('/band/<int:id>/delete')
def delete_band(id):
    model_bands.Band.delete_one(id)
    return redirect('/')