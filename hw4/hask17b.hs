longest_run :: [Bool] -> Int
longest_run lst = helper lst 0 0
    where
        helper :: [Bool] -> Int -> Int -> Int
        helper [] curr_len max_len = max curr_len max_len
        helper (x:xs) curr_len max_len
            | x == True  = helper xs (curr_len + 1) max_len
            | otherwise  = helper xs 0 (max curr_len max_len)
