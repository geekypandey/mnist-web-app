#Rule : Always validate the input on server side.Always.Don't trust the user!
import os
import pathlib
import time

from flask import Flask,render_template,request,flash,redirect
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms import SubmitField,MultipleFileField
from werkzeug.utils import secure_filename
from fastai.vision import *

UPLOAD_FOLDER = os.path.join('static','images')
path = pathlib.Path('models/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret_key'

bootstrap = Bootstrap(app)

class PhotoForm(FlaskForm):
    photo = MultipleFileField()
    submit = SubmitField('Upload')

@app.before_first_request
def init():
    defaults.device = torch.device('cpu')
    global learn
    print('Loaded')
    learn = load_learner(path,'mnist.pkl')


@app.route('/',methods=['POST','GET'])
def index():
    form = PhotoForm()
    output = {}
    if form.validate_on_submit():
        uploaded_files = request.files.getlist("photo")
        for file in uploaded_files:
            if file:
                filename = secure_filename(file.filename)
                img_src = os.path.join('static/images',filename)
                file.save(img_src)
                image = open_image(img_src)
                pred_class,pred_idx,outputs = learn.predict(image)
                output[file.filename] = pred_class
        return render_template('output.html',output=output)
    return render_template('index.html',form=form)  

if __name__ == '__main__':
    app.run(debug=True)
