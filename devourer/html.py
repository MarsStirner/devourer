# -*- coding: utf-8 -*-

from flask import render_template, send_file

from devourer.systemwide import app
from devourer.lib.files import get_file_info, get_full_file_path


@app.route('/')
def index():
    return u'Подсистема хранения файлов'


@app.route('/upload_form.html')
def html_upload_form():
    return render_template('upload_form.html')


@app.route('/file/<fileid>')
def serve_file(fileid):
    try:
        fileinfo = get_file_info(fileid)
        if not fileinfo:
            raise IOError
        return send_file(
            get_full_file_path(fileid),
            as_attachment=True,
            attachment_filename=fileinfo['name'].encode('utf-8')
        )
    except IOError:
        return u'Файл не найден'
