#!/usr/bin/python
from flask import Flask, jsonify
import gviz_api
import datetime

app = Flask(__name__)

table = {"time":   ("datetime", "Time"),
         "temp":   ("number",   "Temp")}

data = [{"time": datetime.datetime(2015,12,30,10,0,0,0), "temp": (66.1, "66.1 F")},
        {"time": datetime.datetime(2015,12,30,10,1,0,0), "temp": (68.3, "68.3 F")}]

@app.route('/')
def index():
    data_table = gviz_api.DataTable(table)
    data_table.LoadData(data)
    resp = app.make_response(data_table.ToJSon(columns_order=("time", "temp"),order_by="time"))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
