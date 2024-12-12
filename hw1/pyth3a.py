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


class FakeDuck:
  def quack(self):
    pass
  
fake_duck = FakeDuck()
print(is_duck_a(fake_duck))
print(is_duck_b(fake_duck))