sum_is_divisible :: Int -> Int -> Int -> Bool
sum_is_divisible a b c = sum_range a b `mod` c == 0
    where
        sum_range :: Int -> Int -> Int
        sum_range a b
            | a > b = 0
            | otherwise = a + sum_range (a + 1) b