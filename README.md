# dynamic_calendar
A calendar that allows scheduling of dynamic events - Python3


Event:
    Dynamic
    Static

Server:
    Create Event //Post -> Done
    Update Event //Put  -> Done
    Delete Event //Delete -> Done
    Get Calendar -> In Progress

Backend:
    Organize / Stringify Events using python classes/magic methods


login page:
    request user calendar using id as param -> Done


Calendar page:
    To-do-list -> Done
    Calendar page - Emulate To-do-list
    Settings page ?


Things to Fix:
    Returns for bad inputs
    Add static event link start and end time possibly


Notes on Dynamic Additions:
    Dynamic calendar additions only consider the hour (rounded up for the event's end time)
    If date has passed, it is not added to the calendar
    Dynamic additions are done on the backend to utilize python, but in practice, they should be done on the front end so that the page does not need to be reloaded in order to see changes. (This would also present a heavy load on the server as non-trivial computations are done)
