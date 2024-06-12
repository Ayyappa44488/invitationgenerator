from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
# hostname = 'localhost'
# username = 'root'
# password = 'Ayyappa2003'
# port=3306
# database = 'carddesign'

# cnx=create_engine(f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}')
# conn=cnx.connect()
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Ayyappa2003@localhost:3306/carddesign'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
