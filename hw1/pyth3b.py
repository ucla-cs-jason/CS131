class Duck:
  def __init__(self):
    pass # Empty initializer


def is_duck_a(duck):
  try:
    duck.quack()
    return True
  except:
    return False


def is_duck_b(duck):
  return isinstance(duck, Duck)


class RoastDuck(Duck):
  def roast():
    pass
  
roast_duck = RoastDuck()
print(is_duck_a(roast_duck))
print(is_duck_b(roast_duck))