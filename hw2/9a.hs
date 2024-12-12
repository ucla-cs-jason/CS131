fibonacci :: Int -> [Int]
fibonacci n
    | n <= 0 = []
    | otherwise = reverse (f n [1, 1])
    where
        f :: Int -> [Int] -> [Int]
        f 2 lst = lst
        f m (x:y:xs) = f (m - 1) ((x + y):x:y:xs)