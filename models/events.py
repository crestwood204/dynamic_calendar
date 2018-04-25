''' event classes '''
import datetime
from functools import total_ordering


@total_ordering
class Dynamic_Event():
    def __init__(self, id, title, due_date, duration):
        self._id = id
        self._title = title
        self._due_date = due_date
        self._duration = duration
        self._assigned_time = None
        self._assigned_date = None
        self._end_time = None

    def get_id(self):
        return self._id

    def __eq__(self, other):
        sdd = self._due_date.split('-')
        odd = other._due_date.split('-')
        return (datetime.date(int(sdd[0]), int(sdd[1]), int(sdd[2])) ==
                datetime.date(int(odd[0]), int(odd[1]), int(odd[2])))

    def __gt__(self, other):
        sdd = self._due_date.split('-')
        odd = other._due_date.split('-')
        return (datetime.date(int(sdd[0]), int(sdd[1]), int(sdd[2])) >
                datetime.date(int(odd[0]), int(odd[1]), int(odd[2])))

    def get_title(self):
        return "d': " + self._title

    def get_due_date(self):
        return self._due_date

    def get_duration(self):
        return self._duration

    def get_start_time(self):
        return self._assigned_time

    def get_end_time(self):
        return self._end_time

    def set_assigned_time(self, time):
        self._assigned_time = '{}:00'.format(time)
        new_time = time + int(self._duration)
        self._end_time = '{}:00'.format(new_time)

    def get_start_date(self):
        return self._assigned_date

    def get_end_date(self):
        return self._assigned_date

    def set_assigned_date(self, date):
        self._assigned_date = date

    def get_event_type(self):
        return 'dynamic'


@total_ordering
class Static_Event():
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
        return datetime.datetime(int(sd[0]), int(sd[1]), int(sd[2]),
                                 int(st[0]), int(st[1]))

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

    def get_event_type(self):
        return 'static'

    def __str__(self):
        # process datetime object to get date and time
        return '{} at {} to {} at {}: {}'.format(self._start_date,
                                                 self._start_time,
                                                 self._end_date,
                                                 self._end_time, self._title)


def order_events(start_time, end_time, dvents, svents):
    total_events = []
    # sort the static events
    static_events = []
    for svent in svents:
        static_events.append(Static_Event(svent["id"], svent["title"],
                                          svent["start_date"],
                                          svent["end_date"],
                                          svent["start_time"],
                                          svent["end_time"]))
    static_events = sorted(static_events)

    # sort the dynamic events
    dynamic_events = []
    for dvent in dvents:
        if dvent["due_date"] is not None and dvent["duration"] is not None:
            dynamic_events.append(Dynamic_Event(dvent["id"], dvent["title"],
                                                dvent["due_date"],
                                                dvent["duration"]))
    dynamic_events = sorted(dynamic_events)

    # Loop over time and check static events for overlaps
    day = datetime.date.today()
    time = start_time
    curr_time = int(str(datetime.datetime.now().time()).split(':')[0]) + 1
    if time < curr_time:
        time = curr_time
    for dvent in dynamic_events:
        duration = int(dvent.get_duration())
        due_date = dvent.get_due_date()
        due_dd = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        # date has passed
        if due_dd < day:
            continue

        # assign the event
        while(due_dd >= day):
            # if there is a static event, consider it
            if len(static_events) > 0:
                svent = static_events[0]
                svent_start_date = datetime.datetime.strptime(
                                                    svent.get_start_date(),
                                                    "%Y-%m-%d").date()
                svent_end_date = datetime.datetime.strptime(
                                                    svent.get_end_date(),
                                                    "%Y-%m-%d").date()
                svent_start_hr = int(svent.get_start_time().split(':')[0])
                svent_end_hr = int(svent.get_end_time().split(':')[0])
                if int(svent.get_end_time().split(':')[1]) != 0:
                    svent_end_hr += 1
                # next static event has yet to occur - add dynamic event
                if day < svent_start_date:
                    if time + duration <= end_time:
                        dvent.set_assigned_date(str(day))
                        dvent.set_assigned_time(time)
                        total_events.append(dvent)
                        time += duration
                        break
                    else:  # if not enough time in day, increment day and loop
                        day = day + datetime.timedelta(days=1)
                        time = start_time

                # next static event occurred or is occuring, remove it
                if day > svent_start_date:
                    if day > svent_end_date:
                        total_events.append(static_events.pop(0))
                    if day < svent_end_date:
                        day = day + datetime.timedelta(days=1)
                    if day == svent_end_date:
                        # check when event ends
                        time = svent_end_hr

                        if time + duration <= end_time:
                            dvent.set_assigned_date(str(day))
                            dvent.set_assigned_time(time)
                            time += duration
                            total_events.append(static_events.pop(0))
                            total_events.append(dvent)
                            break
                        else:
                            day = day + datetime.timedelta(days=1)
                            total_events.append(static_events.pop(0))

                # curr_day is the day that this event starts on
                if day == svent_start_date:
                    # try to add event before start time
                    if time + duration < svent_start_hr and (time + duration
                                                            <= end_time):
                        dvent.set_assigned_date(str(day))
                        dvent.set_assigned_time(time)
                        time += duration
                        total_events.append(dvent)
                        break
                    # if event ends on this day, try after event ends
                    elif svent_start_date == svent_end_date:
                        # check when event ends
                        time = svent_end_hr
                        # add event
                        total_events.append(static_events.pop(0))
                    # event ends on future day
                    elif svent_start_date < svent_end_date:
                            day = day + datetime.timedelta(days=1)
                    # event ended in the past?
                    elif svent_start_date > svent_end_date:
                        static_events.pop(0)  # invalid event
            # assign dynamic event
            else:
                if time + duration <= end_time:
                    dvent.set_assigned_date(str(day))
                    dvent.set_assigned_time(time)
                    total_events.append(dvent)
                    time += duration
                    break
                else:  # if not enough time in day: increment day, start over
                    day = day + datetime.timedelta(days=1)
                    time = start_time
    for svent in static_events:
        total_events.append(svent)
    return total_events
