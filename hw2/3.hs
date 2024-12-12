is_odd_if :: Integer -> Bool
is_odd_if num = do
    if num == 0
        then False
    else is_even_if (num - 1)

is_even_if :: Integer -> Bool
is_even_if num = do
    if num == 0
        then True
    else is_odd_if (num - 1)

is_odd_guard :: Integer -> Bool
is_odd_guard num
    | num == 0 = False
    | otherwise = is_even_guard (num - 1)

is_even_guard :: Integer -> Bool
is_even_guard num
    | num == 0 = True
    | otherwise = is_odd_guard (num - 1)

is_odd_pattern :: Integer -> Bool
is_odd_pattern 0 = False
is_odd_pattern num = is_even_pattern (num - 1)

is_even_pattern :: Integer -> Bool
is_even_pattern 0 = True
is_even_pattern num = is_odd_pattern (num - 1)
