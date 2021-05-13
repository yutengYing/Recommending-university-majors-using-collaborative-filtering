import os
import uuid

from flask import Flask, flash, session, redirect, url_for, send_from_directory
from flask import render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

from bookmark_analysis import BookMark
from src.Recommend import Applicant, MajorRecommender

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'bookmark')


@app.route("/", methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.bookmark.data
        filename = random_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_PATH'], filename)
        f.save(filepath)
        bk = BookMark(str(filepath))
        bk.html_to_markdown()
        bk.keep_title()
        filepath = bk.get_markdown_name()
        scores = form.scores.data
        flash('Upload success.')
        session['filenames'] = filepath
        session['scores'] = scores
        return redirect(url_for('recommend'))
    return render_template('upload.html', form=form)


@app.route('/recommend')
def recommend():
    appliacnt = Applicant(session['scores'], session['filenames'])
    mr = MajorRecommender()
    appliacnt_recommend_list = mr.recommend_for(appliacnt)
    return render_template('recommend.html', appliacnt_recommend_list=appliacnt_recommend_list)


@app.route('/upload/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH', filename])


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


class UploadForm(FlaskForm):
    bookmark = FileField('Upload bookmark_file', validators=[FileRequired(), FileAllowed(['html'])])
    scores = StringField('Type your scores', validators=[DataRequired()])
    submit = SubmitField('Recommend for me')


if __name__ == '__main__':
    app.run(debug=True)
