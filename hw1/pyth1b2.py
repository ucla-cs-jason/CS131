import copy

class Comedian:
  def __init__(self, joke):
    self.__joke = joke

  def change_joke(self, joke):
    self.__joke = joke

  def get_joke(self):
    return self.__joke

def process(c):
 # c = [joke1, joke2]
 c = copy.copy(c)
 # out c = [joke1, joke2]
 # c = [joke1, joke2]
 c[1] = Comedian("joke3")
 # out c = [joke1, joke2]
 # c = [joke1, joke3]
 c.append(Comedian("joke4"))
 # out c = [joke1, joke2]
 # c = [joke1, joke3, joke4]
 c = c + [Comedian("joke5")]		
 # out c = [joke1, joke2]
 # unpointed c = [joke1, joke3, joke4]
 # c = [joke1, joke3, joke4, joke5]
 c[0].change_joke("joke6")
 # out c = [joke6, joke2]
 # unpointed c = [joke6, joke3, joke4]
 # c = [joke6, joke3, joke4, joke5]

def main():
 c1 = Comedian("joke1")
 c2 = Comedian("joke2")
 com = [c1,c2]
 process(com)
 c1 = Comedian("joke7")
 for c in com:
  print(c.get_joke())

main()