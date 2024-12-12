rle :: [Int] -> [(Int, Int)]
rle [] = []
rle lst = tail (f lst 0 0)
    where
        f :: [Int] -> Int -> Int -> [(Int, Int)]
        f [] prev_element prev_count = [(prev_element, prev_count)]
        f (x:xs) prev_element prev_count
            | x == prev_element = f xs prev_element (prev_count + 1)
            | otherwise = (prev_element, prev_count) : (f xs x 1)