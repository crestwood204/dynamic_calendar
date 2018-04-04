from models.events import *
import datetime

#need to store static and dynamic events in cloud
dynamic_events = []
static_events = []

new_dvent = Dynamic_Event("hello", "check", "Towne 100")
print(new_dvent.GetType())
