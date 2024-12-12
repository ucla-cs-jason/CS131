find_min :: [Int] -> Int
find_min [x] = x
find_min (x:xs) = 
    let min_rest = find_min xs
    in if x < min_rest then x else min_rest