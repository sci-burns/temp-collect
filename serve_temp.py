#!/usr/bin/python
from flask import Flask, jsonify
import gviz_api
from datetime import *
from time import *

fileName = "test.csv"

app = Flask(__name__)

table = {"time":   ("datetime", "Time"),
         "temp":   ("number",   "Temp")}

data = []

def readLines():
    data = []
    myFile = open(fileName, 'r')
    lines = myFile.readlines()
    myFile.close()

    for line in lines:
        entry = {}
        fields = line.rstrip().split(',')
        theTime = strptime(fields[0].rstrip(), "%Y-%m-%d %H:%M:%S")
        entry["time"] = datetime.fromtimestamp(mktime(theTime))
        entry["temp"] = (float(fields[1]), fields[1].rstrip() + " F")
        data.append(entry)

@app.route('/')
def index():
    readLines()
    data_table = gviz_api.DataTable(table)
    data_table.LoadData(data)
    resp = app.make_response(data_table.ToJSon(columns_order=("time", "temp"),order_by="time"))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
