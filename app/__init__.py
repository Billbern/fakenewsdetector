
import os
import torch
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
import jwt

# import MLP module definition
from app.utils.custpickle import CustomUnpickler
from app.utils.preprocessor import preprocess
from app.config import DevConfig, ProdConfig

# load saved model parameters and vectorizers
current_wd = os.getcwd()
model = CustomUnpickler( open(f'{current_wd}/app/data/multi-layer-perceptron-parameters.pkl', 'rb') ).load()
text_vectorizer = CustomUnpickler( open(f'{current_wd}/app/data/text_vectorizer.pkl', 'rb') ).load()


app = Flask(__name__, static_url_path="/static")
app.config.from_object(DevConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from app.models.user import User
from app.models.article import Article

try:
    db.create_all()
except Exception as e:
    print(f'\n\n Error {e} \n\n')


@app.route('/')
def home():
    if "token" in request.cookies.keys():
        return redirect('/dashboard')
    else:
        return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    if "token" in request.cookies.keys():
        decoder = jwt.decode(request.cookies["token"], os.environ.get("APP_SECRET"), algorithms=["HS256"])
        if decoder['whoami']:
            articles = Article.query.all()
            print(articles)
            return render_template('dashboard.html', articles=articles)
        else:
            resp = make_response(redirect('/'))
            resp.set_cookie('token', '', expires=0)
            return resp
    else:
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    if username and password :
        try:
            prosAdmin = User.query.filter_by(username=username).first()
            if prosAdmin:
                if prosAdmin.password == password:
                    token = jwt.encode({'whoami': prosAdmin.username }, os.environ.get("APP_SECRET"), algorithm="HS256")
                    return jsonify({"Success": {"user": prosAdmin.username, "token": token }})
                else:
                    return jsonify({"Error": 'Wrong Username or Password'})
            else:
                return jsonify({"Error": 'Wrong Username or Password'})
        except Exception as e:
            print(e)
    else:
        return jsonify({"Error": 'Inputs should not be empty'})
        


    return redirect('/')


@app.route('/predict', methods=['POST'])
def predict():
    text = request.json['text']
    checkArticle = Article.query.filter_by(text=text).first()

    if checkArticle:
        return jsonify({ "result": checkArticle.authenticity })
    else:
        d = {'text': [text]}

        # create dataframe from user input
        X_df = pd.DataFrame(data=d)

        # preprocess df and return np array
        X_np = preprocess(X_df, text_vectorizer)

        # convert to tensor
        X_tensor = torch.Tensor(X_np)

        # predict
        y_pred = model(X_tensor)
        y_pred_max = torch.max(y_pred, 1)[1]

        if y_pred_max == 1:
            result = "real"
        else:
            result = "fake"

        today = datetime.now()
        newArticle = Article(text, request.remote_addr, result, today.strftime("%d-%m-%Y"))
        db.session.add(newArticle)
        db.session.commit()
        
        return jsonify({"result": result})
