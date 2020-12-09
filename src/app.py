# Import Dependencies 
from flask import Flask, request, render_template, redirect, jsonify, url_for 
from flask_pymongo import PyMongo
import psycopg2
import sys
from datetime import datetime
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
# import datetime as dt
from dateutil.parser import parse
import sys
import numpy as np
import os
import csv
import ETL
import yfinancex
import word_cloud




# Create an instance of Flask app
app = Flask(__name__)

@app.route('/')
def index():
    word_cloud.Word_Cloud()
    return render_template('index.html')
# @app.route('/tables') 
# def stable():
#     db = client['WallStreet']
#     hp_collection = db["HP"]
#     hdata = hp_collection.find_one()
#     print(hdata)
#     return render_template("tables.html", hdata=hdata)

@app.route('/', methods=['POST']) 
def Stock_Select(): 
    ETL.Stock_Select(request)
    return render_template('index.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/StockETL/')
def StockETL():
    return render_template('StockETL.html')

@app.route('/Searched_Stock/')
def Searched_Stock():
    return render_template('Stocksearch.html')
@app.route('/Searched_Ticker/')
def mSearched_Stock():
    return render_template('ticker.html')

@app.route("/tester.json")
def tester():
    con = psycopg2.connect("host='localhost' dbname='investopedia_db' user='postgres' password='postgres'")  
    cur = con.cursor()
    cur.execute("""select * from  sunburst""")
    # data = [col for col in cur]
    sunburst_obj =[] 
    for response in cur:

         sun_dict= {'id': response[0], 'ids': response[1], 'labels': response[2], 'parents': response[3]}
         sunburst_obj.append(sun_dict)
    cur.close()
    return jsonify(sunburst_obj)
    # db = client.investopedia
    # collection = db.sunburst 
    # for s in collection.find():
    #     parents=[]
    #     for x in s['parents']:
    #         if isinstance(x,float):
    #             a=""
    #         else:
    #             a=x
    #         parents.append(a)
    #     s['parents']=parents
    #     sunburst_obj.append(s)
    

    # response = dumps({"response": sunburst_obj})
    # return response
@app.route('/dashboard')
def dash():

    return render_template('dashboard.html')

@app.route('/frequency/')
def sword():
    return render_template('word.html')

@app.route('/User-Profile/')
def user():

    return render_template('user.html')
@app.route('/gather-stock-data') 
def candle():
        yfinancex.updateTable(request)
        return render_template("symbol.html")



 
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)


