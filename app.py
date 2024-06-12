from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from confidential import mysql_url

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=mysql_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
