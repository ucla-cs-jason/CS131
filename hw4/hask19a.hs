sumSquares :: Integer -> Integer
sumSquares 0 = 0
sumSquares n = n * n + sumSquares (n - 1)