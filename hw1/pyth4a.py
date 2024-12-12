def largest_sum(nums, k):
  if k < 0 or k > len(nums):
    raise ValueError
  elif k == 0:
    return 0

  max_sum = None
  for i in range(len(nums)-k+1):
    sum = 0
    for num in nums[i:i+k]:
      sum += num
    if not max_sum or sum > max_sum:
      max_sum = sum
  return max_sum

print(largest_sum([3,5,6,2,3,4,5], 3))
print(largest_sum([10,-8,2,6,-1,2], 4))