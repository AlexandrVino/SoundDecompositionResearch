from flask import Flask, render_template, redirect, make_response, jsonify, request, flash
from werkzeug.utils import secure_filename
import requests
import os
from utils.full_algorythm import full_algorythm

UPLOAD_FOLDER = 'downloads'
ALLOWED_EXTENSIONS = {'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'the random string'


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Show main page"""
    return render_template("index.html")


@app.route("/solve", methods=["GET", "POST"])
def solve():
    """Show main page"""
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect("/")
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return render_template("index.html")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        data = full_algorythm(file_path)
        os.remove(file_path)
        return render_template("result.html", data=data, song_name=filename.replace("_", " "))

    
def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
