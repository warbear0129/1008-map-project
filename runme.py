import pip
for module in ["flask", "json"]:
    try:
        __import__(module)
        
    except ImportError:
        print("{} not installed, installing ...".format(module))
        pip.main(["install", "flask"])
        
        
import flask
import json
import db
from algorithms import *
from objects import *

app = flask.Flask(__name__)
db = db.Database()

@app.route("/")
def main_page():
    return flask.render_template("main.html")

@app.route("/api/nodes/all", methods=["GET"])
def all_nodes():
    return json.dumps(db.select_many("SELECT * FROM nodes ORDER BY name"))

@app.route("/api/nodes/id/<id>", methods=["GET"])
def id_nodes(id):
    data = db.select_one("SELECT * FROM nodes WHERE id = '{}'".format(id))
    
    if data is None:
        return {"Error": "Node not found"}
    
    return data

@app.route("/api/path/<source>/<destination>", methods=["GET"])
def get_path(source, destination):
    source = db.select_node(id=source)
    destination = db.select_node(id=destination)
    adj_list = db.select_adj_list()
    a = Dijkstra(source, destination, Graph(data=adj_list), ListPriorityQueue())
    result = a.getPath()
    
    if result == []:
        return {"Error": "No possible routes"}
    
    return json.dumps(result, default=lambda o: o.__dict__)

app.run()