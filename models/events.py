''' event classes '''
import datetime
from functools import total_ordering

class Event(object):
    def __init__(self, title, type, location):
        self._title = title
        self._type = type
        self._location = location
        pass

    def GetTitle(self):
        return self.title

    def GetType(self):
        return self.type

    def GetLocation(self):
        return self.location


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
    def __init__(self, title, type, location, date):
        super().__init__(title, type, location)
        self._date = date

    def GetTitle(self):
        return super(Static_Event, self).GetTitle()

    def GetType(self):
        return super(Static_Event, self).GetType()

    def GetLocation(self):
        return super(Static_Event, self).GetLocation()

    def __eq__(self, other):
        return (self.date == other.date)

    def __gt__(self, other):
        return (self.date > other.date)
