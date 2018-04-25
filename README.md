# dynamic_calendar
A calendar that allows scheduling of dynamic events - Python3

Modules Used:
    functools in 'models/events.py' - line 6, 20-30, 65, 75-79
    datetime in 'models/events.py' - line 6, 20-30, 65, 75-79, 138-234
    flask in server.py - line 8-243
    pymongo - line 10-11, 53-67, etc.
    bson - line 77, 115, 120, 145, 151, etc.
    os - line 10

Name and Location of Custom Class:
    /models/events.py: Dynamic_Event and Static_Event

Name and Location of Decorators:
    I used the @total_ordering decorator from functools in /models/events.py
    In addition, I used the @app.route and @app.errorhandler decorators from flask in server.py

Project Features:
    Login Page / Signup Page - username/password
        -javascript ajax requests to the server's api
        -response based on database request from the server
    To-do-list + calendar view
        -creation, modification, and deletion of static and dynamic items
            -done using ajax requests to the server
            -some server-side validation implemented
            -server then queries/modifies the database in response
        -automatic sorting of events
            -inserts dynamic events into the list of static events
        -Jinja used for utilizing python objects within html
        -Bootstrap grid used to keep everything ordered into rows and columns
            -cdn used for jquery and bootstrap on the frontend
        -Updates are not dynamic. Due to "Notes on Dynamic Additions" below, I
         did not implement dynamic additions/edits to the page. Therefore,
         one must reload to see changes made.
    Git
        The entire project was created utilizing git version control
        https://github.com/crestwood204/dynamic_calendar
        However, the project on github does not contain the env.sh file, so
        you would need to source your own MONGODB_URI to get this to work after
        cloning the repository.

How to launch / operate the project:
    -Open terminal and navigate to the dynamic_calendar directory
    -source <env.sh>
    -export FLASK_APP=server.py
    -flask run
    -Open web browser and go to localhost:5000 (Designed for Google Chrome)
    -Create an account and login
    -Once logged in, click on the plus signs to add static vs dynamic events
    -Reload the page to see changes.

Notes on Dynamic Additions:
    Dynamic calendar additions only consider the hour (rounded up for the event's end time)
    If date has passed, it is not added to the calendar
    Dynamic additions are done on the backend to utilize python, but in practice, they should be done on the front end so that the page does not need to be reloaded in order to see changes. (This would also present a heavy load on the server as non-trivial computations are done)
