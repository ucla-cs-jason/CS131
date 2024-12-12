all_factors :: Int -> [Int]
all_factors num = [x | x <- [1..num], num `mod` x == 0]

perfect_numbers :: [Int]
perfect_numbers = [x | x <- [1..], sum(init(all_factors x)) == x]