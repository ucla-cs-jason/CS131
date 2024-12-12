data Quest = Subquest Quest | FinalBoss

count_subquests :: Quest -> Integer
count_subquests FinalBoss = 0
count_subquests (Subquest quest) = 1 + count_subquests quest

data InstagramUser = 
    Influencer { sponsors :: [String], followers :: [InstagramUser] } | 
    Normie