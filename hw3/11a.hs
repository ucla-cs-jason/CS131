-- count_if (\x -> mod x 2 == 0) [2, 4, 6, 8, 9] should return 4.
-- count_if (\x -> length x > 2) ["a", "ab", "abc"] should return 1.
count_if :: (a -> Bool) -> [a] -> Int
count_if predicate [] = 0
count_if predicate (x:xs)
    | predicate x = 1 + count_if predicate xs
    | otherwise = count_if predicate xs

