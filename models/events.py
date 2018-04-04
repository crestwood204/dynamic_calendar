''' event classes '''

class Event(object):
    def __init__(self, title, type, location):
        self.title = title
        self.type = type
        self.location = location
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

class Static_Event(Event):
    def __init__(self, title, type, location):
        super().__init__(title, type, location)
