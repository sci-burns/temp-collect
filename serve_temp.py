#!/usr/bin/python
from flask import Flask
import gviz_api
from datetime import *
from time import *
#import time

fileName = "test.csv"

app = Flask(__name__)

table = {"time":   ("datetime", "Time"),
         "temp":   ("number",   "Temp")}

data = []

def readLines():
    try:
        myFile = open(fileName, 'r')
        lines = myFile.readlines()
        myFile.close()
        print "clean read " + str(len(lines))
    except:
        print "Exception?"
        lines = "except"

    return lines

def scrapeData():
    data = []
    lines = readLines()

    if lines == "except":
        print "sleeping for 5 second...."
        time.sleep(5)
        lines = readLines()

    print "scrapping..." + str(len(lines))
    for line in lines:
        entry = {}
        fields = line.rstrip().split(',')
        theTime = strptime(fields[0].rstrip(), "%Y-%m-%d %H:%M:%S")
        entry["time"] = datetime.fromtimestamp(mktime(theTime))
        entry["temp"] = (float(fields[1]), fields[1].rstrip() + " F")
        data.append(entry)
    print "done scrapping..."
    print data

@app.route('/')
def index():
    scrapeData()
    data_table = gviz_api.DataTable(table)
    data_table.LoadData(data)
    resp = app.make_response(data_table.ToJSon(columns_order=("time", "temp"),order_by="time"))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

