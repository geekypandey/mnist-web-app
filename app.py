import os
import pathlib
from flask import Flask,render_template,request,flash,redirect
from werkzeug.utils import secure_filename
from fastai.vision import *


UPLOAD_FOLDER = os.path.join('static','images')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
path = pathlib.Path('models/')

@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        else:
            file = request.files['file'] 
            filename = secure_filename(file.filename)
            img_src = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(os.path.join(img_src))
            image = open_image(img_src)
            defaults.device = torch.device('cpu')
            learn = load_learner(path,'mnist.pkl')
            pred_class,pred_idx,outputs = learn.predict(image)
            return render_template('output.html',output=pred_class)
    return render_template('index.html')  

if __name__ == '__main__':
    app.run(debug=True)
