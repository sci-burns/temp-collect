#!/usr/bin/python
from flask import Flask
import gviz_api
from datetime import *
from time import *
import time

fileName = "test.csv"

app = Flask(__name__)

table = {"time": ("datetime", "Time"),
         "temp": ("number", "Temp")}

data = []


def readlines():
    try:
        myfile = open(fileName, 'r')
        lines = myfile.readlines()
        myfile.close()
        print "clean read " + str(len(lines))
    except:
        print "Exception?"
        lines = "except"

    return lines


def scrapedata():
    del data[:]
    lines = readlines()

    if lines == "except":
        print "sleeping for 5 second...."
        time.sleep(5)
        lines = readlines()

    for line in lines:
        entry = {}
        fields = line.rstrip().split(',')
        thetime = strptime(fields[0].rstrip(), "%Y-%m-%d %H:%M:%S")
        entry["time"] = datetime.fromtimestamp(mktime(thetime))
        entry["temp"] = (float(fields[1]), fields[1].rstrip() + " F")
        data.append(entry)


@app.route('/')
def index():
    print "begin request..."
    scrapedata()
    data_table = gviz_api.DataTable(table)
    data_table.LoadData(data)
    resp = app.make_response(data_table.ToJSon(columns_order=("time", "temp"), order_by="time"))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True)

    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()
