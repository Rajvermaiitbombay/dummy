# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 15:28:15 2018

@author: logistics
"""
import os
import pandas as pd
import numpy as np
import flask
import pickle,json
from flask import Flask, render_template, url_for, request, jsonify,flash,send_file,Response
import sklearn
from sklearn.externals import joblib
import glob
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt

app=Flask(__name__)
@app.route('/')
def student():
   return render_template('main.html')
if __name__ == '__main__':
    port=int(os.environ.get('PORT',5000))
    app.run(host='127.0.0.1',port=port)
