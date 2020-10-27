# -*- coding: utf-8 -*-
"""
Index Module
------------
"""
from flask import (
    Blueprint, redirect, render_template, request, session, url_for, abort
)
from picture.pic import get_picture_name

bp = Blueprint('site', __name__)


@bp.route('/')
def index():
    picture_name = get_picture_name()
    return render_template('site/index.html', picture_name=picture_name)
