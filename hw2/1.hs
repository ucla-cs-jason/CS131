largest :: String -> String -> String
largest str1 str2
    | length str1 >= length str2 = str1
    | otherwise = str2