''' event classes '''
import datetime
from functools import total_ordering

class Event(object):
    def __init__(self, title):
        self._title = title
        pass

    def GetTitle(self):
        return self.title


class Dynamic_Event(Event):
    def __init__(self, title, type, location):
        super().__init__(title, type, location)

    def GetTitle(self):
        return super(Dynamic_Event, self).GetTitle()

    def GetType(self):
        return super(Dynamic_Event, self).GetType()

    def GetLocation(self):
        return super(Dynamic_Event, self).GetLocation()


@total_ordering
class Static_Event(Event):
    def __init__(self, id, title, start_date, end_date, start_time, end_time):
        self._id = id
        self._title = title
        self._start_date = start_date
        self._end_date = end_date
        self._start_time = start_time
        self._end_time = end_time

    def __eq__(self, other):
        return self.get_datetime() == other.get_datetime()

    def __gt__(self, other):
        return self.get_datetime() > other.get_datetime()

    def get_datetime(self):
        sd = self._start_date.split('-')
        st = self._start_time.split(':')
        return datetime.datetime(int(sd[0]), int(sd[1]), int(sd[2]), int(st[0]), int(st[1]))

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    def get_start_time(self):
        return self._start_time

    def get_end_time(self):
        return self._end_time

        
    def  __str__(self):
        #process datetime object to get date and time
        return '{} at {} to {} at {}: {}'.format(self._start_date, self._start_time, self._end_date, self._end_time, self._title)


def order_events(start_time, end_time, dvents, svents):
    #sort the static events
    static_events = []
    for svent in svents:
        static_events.append(Static_Event(svent["id"], svent["title"], svent["start_date"], svent["end_date"], svent["start_time"], svent["end_time"]))
    static_events = sorted(static_events)
    return static_events

    #initialize current time


    #go through svents to find current svent
    #check for star_day / end_day

    #for each dvent, assign time based on svent, start/end day and delay

    #keep ordering and return an array of the string representaiton for each event
