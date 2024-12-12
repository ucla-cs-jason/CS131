-- count_if_with_fold (\x -> mod x 2 == 0) [2, 4, 6, 8, 9] should return 4.
-- count_if_with_fold (\x -> length x > 2) ["a", "ab", "abc"] should return 1.
count_if_with_fold :: (a -> Bool) -> [a] -> Int
count_if_with_fold predicate nums = foldl (\acc val -> if predicate val then 1 + acc else acc ) 0 nums