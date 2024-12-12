sumSquares :: Integer -> Integer
sumSquares n = helper 0 n
    where
        helper :: Integer -> Integer -> Integer
        helper curr 0 = curr * curr
        helper curr times_left = curr * curr + helper (curr + 1) (times_left - 1)