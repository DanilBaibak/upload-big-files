from flask import Flask, request, render_template, flash, redirect, url_for, jsonify, send_from_directory
from flask_session import Session

from scripts.file_utils import save_file, get_files_for_dir, allowed_file
from scripts.file_utils import STATUS_FAILED
from os.path import realpath, dirname, isfile, join


app = Flask(__name__)
sess = Session()

current_path = dirname(realpath(__file__))
app.config['UPLOAD_FOLDER'] = '{}/uploads'.format(current_path)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/save-file', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        flash('No file part')
        return jsonify(status=STATUS_FAILED)

    file = request.files['files[]']

    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return jsonify(status=STATUS_FAILED)

    # check extension
    if not allowed_file(file.filename):
        flash('Wrong extension')
        return jsonify(status=STATUS_FAILED)

    # save file
    status = save_file(file, app.config['UPLOAD_FOLDER'])

    return jsonify(status=status)


@app.route('/files', methods=['GET'])
def download_files():
    return render_template('downloads.html', files=get_files_for_dir(app.config['UPLOAD_FOLDER']))


@app.route('/uploads/<path:filename>', methods=['GET'])
def download(filename):
    if not isfile(join(app.config['UPLOAD_FOLDER'], filename)):
        flash('File {} does not exist'.format(filename))
        return redirect(url_for('download_files'))

    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)


if __name__ == '__main__':
    app.secret_key = 'AD84nsd(2Dv*2k'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)

    app.run(debug=True, host='0.0.0.0')
