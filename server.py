from flask import Flask, render_template, request, Response, redirect
from pymongo import MongoClient
from models.events import *
import datetime
import os
import requests

app = Flask(__name__)
app.debug = True
client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_default_database()


#log_handler = logging.FileHandler('my_flask.log')


#need to store static and dynamic events in cloud
dynamic_events = []
static_events = []

@app.route("/example", methods=['GET'])
def hello(name=None):
    '''in url it will be /?adj=xxx'''
    adj = request.args.get('adj')
    print(adj)
    return render_template('hello.html', name=name)

@app.route("/", methods=['GET'])
def redirect_to_login():
    return redirect('/login', code=302)

@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/signup", methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route("/test_post", methods=['POST'])
def test_post(name="Elizabeth"):
    new_user = {
        "username": name
    }
    db.users.insert_one(new_user)

@app.route("/new_user", methods=['POST'])
def create_new_user(username=None, password=None):
    if username and password:
        new_user = {
            'username': username,
            'password': password,
            'dynamic_events': [],
            'static_events': []
        }
        db.users.insert_one(new_user)
        return Response({"attempt": "success"}, status=201, mimetype="application/json")
    else:
        return Response({"attempt": "failure"}, status=400, mimetype="application/json")

@app.route("/add_dynamic_event/<int:user_id>", methods=['POST'])
def add_dynamic_event(dynamic_event):
    #TODO:// add to mongodb
    dynamic_events.append(dynamic_event)

@app.route("/add_static_event/<int:user_id>", methods=['POST'])
def add_static_event(static_event):
    #TODO:// add to mongodb
    static_events.append(static_event)

@app.route("/get_dynamic_events/<int:user_id>", methods=['GET'])
def get_dynamic_events():
    return dynamic_events

@app.route("/get_static_events/<int:user_id>", methods=['GET'])
def get_static_events():
    #get events
    return sorted(static_events)

@app.route("/update_dynamic_event/<int:user_id>", methods=['PUT'])
def update_dynamic_event(dynamic_event):
    return 'hello'

@app.route("/update_static_event/<int:user_id>", methods=['PUT'])
def update_static_event(static_event):
    return 'hello'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

def test_import():
    new_dvent = Dynamic_Event("hello", "check", "Towne 100")
    print(new_dvent.GetType())
