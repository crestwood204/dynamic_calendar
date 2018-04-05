from flask import Flask, render_template, request
from pymongo import MongoClient
from models.events import *
import datetime
import os

app = Flask(__name__)
app.debug = True
client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_default_database()


#log_handler = logging.FileHandler('my_flask.log')


#need to store static and dynamic events in cloud
dynamic_events = []
static_events = []

@app.route("/", methods=['GET'])
def hello(name=None):
    '''in url it will be /?adj=xxx'''
    adj = request.args.get('adj')
    print(adj)
    return render_template('hello.html', name=name)

@app.route("/test_post", methods=['POST'])
def test_post(name="Elizabeth"):
    new_user = {
        "username": name
    }
    db.users.insert_one(new_user)

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
