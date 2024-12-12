foo :: Integer -> Integer -> Integer -> (Integer -> a) -> [a]
foo x y z t = map t [x,x+z..y]

foo :: Int -> Int -> Int -> (Int -> a) -> [a]
foo = \x -> \y -> \z -> \t = map t [x,x+z..y]