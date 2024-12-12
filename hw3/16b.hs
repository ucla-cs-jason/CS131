data LinkedList = EmptyList | ListNode Integer LinkedList
  deriving Show

ll_insert :: LinkedList -> Int -> Int -> LinkedList