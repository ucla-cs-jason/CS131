data InstagramUser = 
    Influencer { sponsors :: [String], followers :: [InstagramUser] } | 
    Normie

count_influencers :: InstagramUser -> Int
count_influencers (Normie) = 0
count_influencers (Influencer _ followers) = sum [1 | Influencer _ _ <- followers]