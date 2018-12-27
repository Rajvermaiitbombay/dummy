# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 15:16:56 2018

@author: Rajkumar
"""
import os
os.chdir(os.path.dirname(__file__))
import threading
import webbrowser 
import random
import pandas as pd
import numpy as np
import flask
import pickle,json
from flask import Flask, render_template, url_for,request, jsonify,flash,send_file,Response, session, abort
import sklearn
from sklearn.externals import joblib
import glob
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt
from werkzeug.serving import run_simple
# Read CSV file #####
lsp = pd.read_csv('lsp.csv')

## Split the training and tesing datasets from main datasets
train = lsp.iloc[np.r_[1:11,16:21],3:10]

## import support vector machine #####
from sklearn.svm import SVC
svc= SVC(kernel='rbf')
svc.fit(train.iloc[:,0:6],train.iloc[:,6])
pickle.dump(svc,open("lsp_rfc.pkl","wb"))
my_model = pickle.load(open("lsp_rfc.pkl","rb"))
    
app=Flask(__name__,template_folder='templates')

@app.route('/')
def student():
   return render_template('index.html')
@app.route('/upload')
def upload():
	return render_template('upload.html')
@app.route('/log')
def log():
    return render_template('login.html')
@app.route('/main')
def main():
    return render_template('mainpage.html')
@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('notify.html')
    elif request.form['password'] == 'password' and request.form['username'] == 'admin':
        return render_template('mainpage.html')
    else:
        return render_template('index.html')
test=pd.DataFrame()
@app.route('/predict', methods = ['GET','POST'])
def predict():
    global test
    if request.method == 'GET':
        return render_template('notify.html')
    elif request.method == 'POST' and request.files['myfile']:
        f = request.files['myfile']
        test = pd.read_csv(f)
        df = my_model.predict(test.iloc[:,2:8])
        dt =pd.DataFrame(df)
        test1=test.reset_index(drop=True)

		## concatnate two dataframes into one dataframe
        total=pd.concat([test1,dt],axis=1)
        total.columns = ['Name','Date','x','y','z','xi','yi','zi','prediction']
        return render_template('data.html')
@app.route('/download') # this is a job for GET, not POST
def data_csv():
    return send_file('pred.xlsx',
                     mimetype='xlsx/csv',
                     attachment_filename='pred.xlsx',
                     as_attachment=True)
@app.route('/result')
def result():
    return render_template('table.html',  tables=[test.to_html(classes='data')], titles=test.columns.values)
@app.route('/test')
def test():
    return render_template('test.html',  data=test.to_html(index=False))

if __name__ == '__main__':
    port=5000+ random.randint(0,999)
    url="http://127.0.0.1:{0}".format(port)
    threading.Timer(1.25,lambda:webbrowser.open(url)).start()
    run_simple('127.0.0.1',port, app,use_debugger=True, use_evalex=True)
