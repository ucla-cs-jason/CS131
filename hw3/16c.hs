data LinkedList = EmptyList | ListNode Integer LinkedList
  deriving Show

ll_insert :: LinkedList -> Integer -> Integer -> LinkedList
ll_insert EmptyList _ element = ListNode element EmptyList
ll_insert (ListNode curr_val next) index element
    | index <= 0 = ListNode element (ListNode curr_val next)
    | index == 1 = ListNode curr_val (ListNode element next)
    | otherwise = ListNode curr_val (ll_insert next (index - 1) element)