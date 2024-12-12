data Tree = Empty | Node Integer [Tree]

max_tree_value :: Tree -> Integer
max_tree_value Empty = 0
max_tree_value (Node val children) = foldl max val (map max_tree_value children)