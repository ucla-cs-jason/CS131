def largest_sum(nums, k):
  if k < 0 or k > len(nums):
    raise ValueError
  elif k == 0:
    return 0

  sum = 0
  for num in nums[:k]:
    sum += num

  max_sum = sum
  for i in range(0, len(nums)-k):
    sum -= nums[i]
    sum += nums[i + k]
    max_sum = max(sum, max_sum)
  return max_sum

print(largest_sum([3,5,6,2,3,4,5], 3))
print(largest_sum([10,-8,2,6,-1,2], 4))
