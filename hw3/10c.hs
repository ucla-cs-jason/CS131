largest :: String -> String -> String
largest str1 str2
    | length str1 >= length str2 = str1
    | otherwise = str2


largest_in_list :: [String] -> String
largest_in_list nums = foldl largest "" nums
