from functools import reduce
def convert_to_decimal(bits):
  exponents = range(len(bits)-1, -1, -1)
  nums = [b * 2 ** e for b, e in zip(bits, exponents)]
  return reduce(lambda acc, num: acc + num, nums)

assert convert_to_decimal([1, 0, 1, 1, 0]) == 22
assert convert_to_decimal([1, 0, 1]) == 5
print('Yay')