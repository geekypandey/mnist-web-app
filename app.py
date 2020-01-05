import os
import pathlib

from flask import Flask,render_template,request,flash,redirect
from flask_bootstrap import Bootstrap 
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
from fastai.vision import *

UPLOAD_FOLDER = os.path.join('static','images')
path = pathlib.Path('models/')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret_key'

bootstrap = Bootstrap(app)

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Upload')

@app.route('/',methods=['POST','GET'])
def index():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        img_src = os.path.join('static/images',filename)
        f.save(img_src)
        image = open_image(img_src)
        defaults.device = torch.device('cpu')
        learn = load_learner(path,'mnist.pkl')
        pred_class,pred_idx,outputs = learn.predict(image)
        return render_template('output.html',output=pred_class)
    return render_template('index.html',form=form)  

if __name__ == '__main__':
    app.run(debug=True)
