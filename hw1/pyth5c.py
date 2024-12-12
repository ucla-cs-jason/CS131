class Event:
  def __init__(self, start_time, end_time):
    if start_time > end_time:
      raise ValueError()
    self.start_time = start_time
    self.end_time = end_time

class Calendar:
  def __init__(self):
    self.__events = []

  def get_events(self):
    return self.__events
  
  def add_event(self, event):
    if not isinstance(event, Event):
      raise TypeError()
    else:
      self.__events.append(event)

class AdventCalendar(Calendar):
  def __init__(self, year):
    self.__events = []
    self.year = year

  def get_events(self):
    return self.__events

advent_calendar = AdventCalendar(2022)
print(advent_calendar.get_events())