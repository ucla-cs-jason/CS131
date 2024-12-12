data Event = Travel Integer | Fight Integer | Heal Integer

super_giuseppe :: [Event] -> Integer
super_giuseppe events = helper events 100
    where
        helper :: [Event] -> Integer -> Integer
        helper [] curr_health = curr_health
        helper (x:xs) curr_health
            | curr_health <= 0 = -1
            | otherwise = 
                let is_defensive = curr_health <= 40
                in case x of
                    Travel distance ->
                        if is_defensive
                        then helper xs curr_health
                        else helper xs (min (curr_health + distance `div` 4) 100)
                    Fight loss ->
                        if is_defensive 
                        then helper xs (curr_health - loss `div` 2)
                        else helper xs (curr_health - loss)
                    Heal heal -> helper xs (min (curr_health + heal) 100)