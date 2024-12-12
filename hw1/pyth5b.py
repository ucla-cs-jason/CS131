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



calendar = Calendar()
print(calendar.get_events())
calendar.add_event(Event(10, 20))
print(calendar.get_events()[0].start_time)
try:
  calendar.add_event("not an event")
except TypeError:
  print("Invalid event")