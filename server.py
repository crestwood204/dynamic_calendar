from flask import Flask, render_template, request, Response, redirect
from pymongo import MongoClient
from bson import ObjectId
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
                return '{}'.format(user['_id'])
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
                'event_id': 0,
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

@app.route("/calendar/<string:user_id>", methods=['GET'])
def get_calendar(user_id):
    #get events here and pass in as args to render
    #redirect to calendar with user id in args -> use user id to search in mongo
    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    if existing_user is None:
        return 'error: user does not exist'
    return render_template('calendar.html', dynamic_events=existing_user["dynamic_events"])

@app.route("/add_dynamic_event/<string:user_id>", methods=['POST'])
def add_dynamic_event(user_id):
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    duration = request.form.get('duration')

    # server-side validation
    if int(duration) < 0:
        return 'duration is too small'

    today = datetime.date.today().split('-')
    due_date = due_date.split('-')
    if int(today[0]) < int(due_date[0]):
        return 'year is too small'
    if int(today[0]) == int(due_date[0]):
        if int(today[1]) < int(due_date[1]):
            return 'month is too small'
        if int(today[1]) == int(due_date[1]):
            if int(today[2]) < int(due_date[2]):
                return 'day is too small'


    # add to mongodb

    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    event_id = int(existing_user["event_id"])
    dynamic_events = existing_user["dynamic_events"]
    dynamic_events.append({"id": event_id, "title": title, "due_date": due_date, "duration": duration})
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"dynamic_events": dynamic_events, "event_id": event_id + 1}}, upsert=False)

    return 'success'

@app.route("/add_static_event/<string:user_id>", methods=['POST'])
def add_static_event(user_id):
    #TODO:// add to mongodb
    static_events.append(static_event)

@app.route("/update_dynamic_event/<string:user_id>", methods=['PUT'])
def update_dynamic_event(user_id):
    # server-side validation
    event_id = request.form.get('event_id')
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    duration = request.form.get('duration')

    # add to mongodb

    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    dynamic_events = existing_user["dynamic_events"]
    for index, event in enumerate(dynamic_events):
        if event["id"] == int(event_id):
            dynamic_events[index] = {
                "id": event_id,
                "title": title,
                "due_date": due_date,
                "duration": duration
            }
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"dynamic_events": dynamic_events}}, upsert=False)

    return 'success'

@app.route("/delete_dynamic_event/<string:user_id>", methods=['DELETE'])
def delete_dynamic_event(user_id):
    event_id = request.form.get('event_id')
    print(event_id)
    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    dynamic_events = [x for x in existing_user["dynamic_events"] if x["id"] != int(event_id)]
    print(dynamic_events)
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": {"dynamic_events": dynamic_events}}, upsert=False)
    return 'success'

@app.route("/delete_static_event/<string:user_id>", methods=['DELETE'])
def delete_static_event(user_id):
    return 'hello'

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
