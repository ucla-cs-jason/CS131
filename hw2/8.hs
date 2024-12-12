count_occurrences :: [Int] -> [Int] -> Int
count_occurrences [] _ = 1
count_occurrences _ [] = 0
count_occurrences (x:xs) (y:ys)
    | x == y = count_rest + count_occurrences xs ys
    | otherwise = count_rest
    where count_rest = count_occurrences (x:xs) ys