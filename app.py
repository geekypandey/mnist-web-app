#Rule : Always validate the input on server side.Always.Don't trust the user!
import os
import pathlib
import time
import multiprocessing

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
    global pool
    pool = multiprocessing.Pool(2)

def get_pred(file):
    img = open_image(file)
    pred_class,_,_ = learn.predict(img)
    return pred_class

@app.route('/',methods=['POST','GET'])
def index():
    form = PhotoForm()
    global output 
    global pool
    output = {}
    if form.validate_on_submit():
        uploaded_files = request.files.getlist("photo")
        for file in uploaded_files:
            file.save(f'static/images/{file.filename}')
        uploaded_files = [f'static/images/{file.filename}' for file in uploaded_files]
        predictions = pool.map(get_pred,uploaded_files)
        return render_template('output.html',output=predictions)

    return render_template('index.html',form=form)  



if __name__ == '__main__':
    app.run(debug=True)
