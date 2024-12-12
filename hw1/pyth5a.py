class Event:
  def __init__(self, start_time, end_time):
    if start_time > end_time:
      raise ValueError()
    self.start_time = start_time
    self.end_time = end_time

event = Event(10, 20)
print(f"Start: {event.start_time}, End: {event.end_time}")

try:
  invalid_event = Event(20, 10)
  print("Success")
except ValueError:
  print("Created an invalid event")