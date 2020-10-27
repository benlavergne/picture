# -*- coding: utf-8 -*-
"""
Pic Module
---------------------
"""
import os
import json
import uuid
import pickle

from pathlib import Path

from flask import (
    Blueprint, redirect, render_template, request, abort,
    session, url_for, current_app, send_from_directory
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('pic', __name__, url_prefix='/pic')


def get_picture_name():
    try:
        with open('data.pickle', 'rb') as f:
            # The protocol version used is detected automatically, so we do not have to specify it.
            data = pickle.load(f)
        return data
    except FileNotFoundError:
        with open('data.pickle', 'wb') as f:
            pickle.dump('person.svg', f, pickle.HIGHEST_PROTOCOL)
        return 'person.svg'


def set_picture_name(name):
    with open('data.pickle', 'wb') as f:
        # Pickle the 'name' using the highest protocol available.
        pickle.dump(name, f, pickle.HIGHEST_PROTOCOL)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/avatar')
def avatar():
    picture_name = get_picture_name()
    return render_template('pic/avatar.html', picture_name=picture_name)


@bp.route('/save_avatar', methods=('GET', 'POST'))
def save_avatar():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return json.dumps({'msg': 'No file'})

        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return json.dumps({'msg': 'No file name'})

        if file and allowed_file(file.filename):
            # Generate randon and unique picture indentifier
            # Create picture_id - UUID type 4 - RFC 4122 --> converted to hex string
            picture_id = uuid.uuid4().hex + ".jpeg"

            # Compute complete path
            sub_dir = 'test'
            app_rootdir = os.path.dirname(current_app.instance_path)
            path = os.path.join(app_rootdir, current_app.config['UPLOAD_FOLDER'])
            path = os.path.join(path, sub_dir)

            # Check if there is an existing directory (create it if not)
            Path(path).mkdir(parents=True, exist_ok=True)

            # Remove existing picture if any
            picture_name = get_picture_name()
            if picture_name != 'person.svg':
                os.remove(os.path.join(path, picture_name))

            # Save new picture_id file
            file.save(os.path.join(path, picture_id))
            # Store new picture_id name
            set_picture_name(picture_id)

            return json.dumps({'msg': 'Upload ok'})

    return json.dumps({'msg': 'Wrong request'})


@bp.route('/delete_avatar', methods=('GET', 'POST'))
def delete_avatar():
    if request.method == 'POST':
        picture_name = get_picture_name()
        if picture_name != 'person.svg':
            # Compute complete path
            sub_dir = 'test'
            app_rootdir = os.path.dirname(current_app.instance_path)
            path = os.path.join(app_rootdir, current_app.config['UPLOAD_FOLDER'])
            path = os.path.join(path, sub_dir)
            # Remove picture
            os.remove(os.path.join(path, picture_name))
            # Remove picture_name
            set_picture_name('person.svg')

            return json.dumps({'msg': 'Delete ok'})
        else:
            return json.dumps({'msg': 'Nothing to delete'})

    return json.dumps({'msg': 'Wrong request'})


@bp.route('/picture')
def send_file():
    # Load picture name
    picture_name = get_picture_name()
    # Compute complete path
    sub_dir = 'test'
    app_rootdir = os.path.dirname(current_app.instance_path)
    path = os.path.join(app_rootdir, current_app.config['UPLOAD_FOLDER'])
    path = os.path.join(path, sub_dir)
    return send_from_directory(path, picture_name)
