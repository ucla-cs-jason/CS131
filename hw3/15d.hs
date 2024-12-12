data InstagramUser = 
    Influencer { sponsors :: [String] } | 
    Normie

is_sponsor :: InstagramUser -> String -> Bool
is_sponsor (Influencer sponsors) sponsor = sponsor `elem` sponsors