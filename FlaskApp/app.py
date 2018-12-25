# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 15:16:56 2018

@author: Rajkumar
"""
import os
os.chdir('E:/logisticsnow/dummy/FlaskApp')
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
# Read CSV file #####
lsp = pd.read_csv('E:\logisticsnow\FlaskApp\data\lsp.csv')

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
	if request.method == 'GET':
		return render_template('notify.html')
	else:
		return render_template('upload.html')
@app.route('/log')
def log():
	if request.method == 'GET':
		return render_template('notify.html')
	else:
		return render_template('login.html')
@app.route('/main')
def main():
	if request.method == 'GET':
		return render_template('notify.html')
	else:
		return render_template('mainpage.html')
@app.route('/data')
def data():
	if request.method == 'GET':
		return render_template('notify.html')
	else:
		return render_template('data.html')

@app.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('notify.html')
	elif request.form['password'] == 'password' and request.form['username'] == 'admin':
		return render_template('mainpage.html')
	else:
		return render_template('index.html')

@app.route('/predict', methods = ['GET','POST'])
def predict():
	if request.method == 'GET':
		return render_template('notify.html')
	elif request.method == 'POST' and request.files['myfile']:
		f = request.files['myfile']
		test = pd.read_csv(f)
		df = my_model.predict(test.iloc[:,2:8])
		dt =pd.DataFrame(df)
		test=test.reset_index(drop=True)

		## concatnate two dataframes into one dataframe
		total=pd.concat([test,dt],axis=1)
		total.columns = ['Name','Date','x','y','z','xi','yi','zi','prediction']
		total.to_html('pred.html')
		test.to_html('test.html')
		total.to_excel('pred.xlsx')
		result ='''
		<html>
		<head>
		<title>Result</title>
		</head>
		<link rel="stylesheet" type="text/css" href="static/table.css">
		   <body>
		   <div class="tab">
		   <h1><b>This is your Dataset</b></h1></br>
			<b><a href="/data">Back</a></b>
		   </div> 
		   <div class="set">
		   {table}
		   </div>
		   </body>  
		</html>      
				'''
		with open(r'E:\logisticsnow\dummy\FlaskApp\templates\pred.html','w') as f:
			f.write(result.format(table=total.to_html(classes='mystyle')))
		with open(r'E:\logisticsnow\dummy\FlaskApp\templates\test.html','w') as f:
			f.write(result.format(table=test.to_html(classes='mystyle'))) 
		return render_template('data.html')
@app.route('/download') # this is a job for GET, not POST
def data_csv():
    return send_file('pred.xlsx',
                     mimetype='xlsx/csv',
                     attachment_filename='pred.xlsx',
                     as_attachment=True)
@app.route('/result')
def result():
	if request.method == 'GET':
		return render_template('notify.html')
	else:
		return render_template('pred.html')
@app.route('/test')
def test():
	if request.method == 'GET':
		return render_template('notify.html')
	else:
		return render_template('test.html')

if __name__ == '__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='127.0.0.1',port=port)
