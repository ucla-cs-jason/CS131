data LinkedList = EmptyList | ListNode Integer LinkedList
  deriving Show

ll_contains :: LinkedList -> Integer -> Bool
ll_contains EmptyList _ = False
ll_contains (ListNode curr_val next) val
    | curr_val == val = True
    | otherwise = ll_contains next val