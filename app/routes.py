import os
import time
from app import app
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from app.utils import load_model
from fastai.vision import open_image

from app.forms import PhotoForm


@app.before_first_request
def init():
    global learn
    learn = load_model(app.config['MODEL_PATH'])

@app.route('/',methods=['POST','GET'])
def index():
    form = PhotoForm()
    output = {}
    if form.validate_on_submit():
        uploaded_files = request.files.getlist("photo")
        for file in uploaded_files:
            img_src = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(img_src)
            image = open_image(img_src)
            pred_class , _ , _ = learn.predict(image)
            output[file.filename] = pred_class
        return render_template('output.html', output=output)
    return render_template('index.html', form=form)
