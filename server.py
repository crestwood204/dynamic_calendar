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

#login methods

@app.route("/", methods=['GET'])
def slash():
    return redirect('/login', 302)

@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

@app.route("/login_post", methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        user = db.users.find_one({"username": username})
        if user:
            if user["password"] == password:
                return 'success'
            else:
                return 'incorrect password'
        else:
            return 'user does not exist'
    else:
        return Response({"attempt": "failure"}, status=400, mimetype="application.json")

@app.route("/signup", methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route("/signup_post", methods=['POST'])
def post_signup():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        existing_user = db.users.find_one({"username": username})
        if not existing_user:
            new_user = {
                'username': username,
                'password': password,
                'dynamic_events': [],
                'static_events': []
            }
            db.users.insert_one(new_user)
            return 'success'
        else:
            #TODO:// user already exists ( format response better )
            return 'user already exists'
    else:
        return 'need to provide username and password'

@app.route("/calendar", methods=['GET'])
def get_calendar():
    #get events here and pass in as args to render
    return render_template('calendar.html')
#api calls

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
