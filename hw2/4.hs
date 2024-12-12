quad :: Double -> Double -> Double -> (Double, Double)
quad a b c
    | a == 0 = (0.0, 0.0)
    | b24ac < 0 = (0.0, 0.0)
    | otherwise = (((-b) + sqrt b24ac) / (2 * a), ((-b) - sqrt b24ac) / (2 * a))
    where
        b24ac = b * b - 4 * a * c
