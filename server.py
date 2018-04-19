from flask import Flask, render_template, request, Response, redirect
from pymongo import MongoClient
from bson import ObjectId
from models.events import *
import datetime
import os

app = Flask(__name__)
app.debug = True
client = MongoClient(os.environ['MONGODB_URI'])
db = client.get_default_database()

# login methods


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
        return Response({"attempt": "failure"}, status=400,
                        mimetype="application.json")


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
                'static_events': [],
                'dynamic_start_time': 9,
                'dynamic_end_time': 21
            }
            db.users.insert_one(new_user)
            return 'success'
        else:
            return 'user already exists'
    else:
        return 'need to provide username and password'


@app.route("/calendar/<string:user_id>", methods=['GET'])
def get_calendar(user_id):
    # get events here and pass in as args to render
    # redirect to calendar with userid in args -> use userid to search in mongo
    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    if existing_user is None:
        return 'error: user does not exist'

    start_time = existing_user["dynamic_start_time"]
    end_time = existing_user["dynamic_end_time"]
    dvents = existing_user["dynamic_events"]
    svents = existing_user["static_events"]
    calendar_strings = order_events(start_time, end_time, dvents, svents)
    return render_template('calendar.html',
                           dynamic_events=existing_user["dynamic_events"],
                           calendar_strings=calendar_strings)


@app.route("/add_dynamic_event/<string:user_id>", methods=['POST'])
def add_dynamic_event(user_id):
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    duration = request.form.get('duration')

    # server-side validation
    if duration is not None:
        if float(duration) < 0:
            return 'duration is too small'

    today = str(datetime.date.today()).split('-')

    due_date_val = due_date.split('-')
    if int(today[0]) > int(due_date_val[0]):
        return 'year is too small'
    if int(today[0]) == int(due_date_val[0]):
        if int(today[1]) > int(due_date_val[1]):
            return 'month is too small'
        if int(today[1]) == int(due_date_val[1]):
            if int(today[2]) > int(due_date_val[2]):
                return 'day is too small'

    # add to mongodb
    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    event_id = int(existing_user["event_id"])
    dynamic_events = existing_user["dynamic_events"]
    dynamic_events.append({"id": event_id, "title": title,
                           "due_date": due_date, "duration": duration})
    db.users.update_one({"_id": ObjectId(user_id)},
                        {"$set": {"dynamic_events": dynamic_events,
                                  "event_id": event_id + 1}}, upsert=False)

    return 'success'


@app.route("/add_static_event/<string:user_id>", methods=['POST'])
def add_static_event(user_id):
    title = request.form.get('title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    # server validation

    start_time_arr = start_time.split(':')
    end_time_arr = end_time.split(':')
    if int(end_time_arr[0]) < int(start_time_arr[0]):
        return 'hour is too small'
    if int(end_time_arr[0]) == int(start_time_arr[0]):
        if int(end_time_arr[1]) < int(start_time_arr[1]):
            return 'min is too small'

    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    event_id = int(existing_user["event_id"])
    static_events = existing_user["static_events"]
    static_events.append({"id": event_id, "title": title,
                          "start_date": start_date, "end_date": end_date,
                          "start_time": start_time, "end_time": end_time})
    db.users.update_one({"_id": ObjectId(user_id)},
                        {"$set": {"static_events": static_events,
                                  "event_id": event_id + 1}}, upsert=False)

    return 'success'


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
        if int(event["id"]) == int(event_id):
            dynamic_events[index] = {
                "id": event_id,
                "title": title,
                "due_date": due_date,
                "duration": duration
            }
            break
    db.users.update_one({"_id": ObjectId(user_id)},
                        {"$set": {"dynamic_events": dynamic_events}},
                        upsert=False)

    return 'success'


@app.route("/update_static_event/<string:user_id>", methods=['PUT'])
def update_static_event(user_id):
    event_id = request.form.get('event_id')
    title = request.form.get('title')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    # add to mongodb

    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    static_events = existing_user["static_events"]
    for index, event in enumerate(static_events):
        if int(event["id"]) == int(event_id):
            static_events[index] = {
                "id": event_id,
                "title": title,
                "start_date": start_date,
                "end_date": end_date,
                "start_time": start_time,
                "end_time": end_time
            }
            break
    db.users.update_one({"_id": ObjectId(user_id)},
                        {"$set": {"static_events": static_events}},
                        upsert=False)

    return 'success'


@app.route("/delete_dynamic_event/<string:user_id>", methods=['DELETE'])
def delete_dynamic_event(user_id):
    event_id = request.form.get('event_id')
    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    dynamic_events = [x for x in existing_user["dynamic_events"]
                      if int(x["id"]) != int(event_id)]
    db.users.update_one({"_id": ObjectId(user_id)},
                        {"$set": {"dynamic_events": dynamic_events}},
                        upsert=False)
    return 'success'


@app.route("/delete_static_event/<string:user_id>", methods=['DELETE'])
def delete_static_event(user_id):
    event_id = request.form.get('event_id')
    existing_user = db.users.find_one({"_id": ObjectId(user_id)})
    static_events = [x for x in existing_user["static_events"]
                     if int(x["id"]) != int(event_id)]
    db.users.update_one({"_id": ObjectId(user_id)},
                        {"$set": {"static_events": static_events}},
                        upsert=False)
    return 'success'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
