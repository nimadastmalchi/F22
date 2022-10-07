-- problem 1a
scale_nums :: [Integer] -> Integer -> [Integer]
scale_nums lst factor = map (* factor) lst

-- problem 1b
only_odds :: [[Integer]] -> [[Integer]]
only_odds lsts = filter (\lst -> all (\x -> (mod x 2 == 1)) lst) lsts

-- problem 1c
largest :: String -> String -> String
largest first second =
    if length first >= length second then first else second

largest_in_list :: [String] -> String
largest_in_list lst = foldr (\str acc -> largest str acc) "" lst

-- problem 2a
count_if :: (a -> Bool) -> [a] -> Int
count_if pred [] = 0
count_if pred (x:xs) = if pred x then 1 + rest else rest
                         where rest = count_if pred xs

-- problem 2b
count_if_with_filter :: (a -> Bool) -> [a] -> Int
count_if_with_filter pred lst = length $ filter pred lst

-- problem 2c
count_if_with_fold :: (a -> Bool) -> [a] -> Int
count_if_with_fold pred lst = foldr
                                (\x acc -> if pred x then acc + 1 else acc)
                                0
                                lst

-- problem 3c
foo :: Integer -> (Integer -> (Integer -> ((Integer -> a) -> [a])))
foo x = \y -> (\z -> (\t -> map t [x,x+z..y]))
foo' x y z t = map t [x,x+z..y]

{-
-- problem 6a
data InstagramUser = Influencer | Normie

-- problem 6b
lit_collab :: InstagramUser -> InstagramUser -> Bool
lit_collab Influencer Influencer = True
lit_collab _ _ = False
--}

{-
-- problem 6c
data InstagramUser = Influencer [String] | Normie

-- problem 6d
is_sponsor :: InstagramUser' -> String -> Bool
is_sponsor (Influencer lst) sponsor = elem sponsor lst
is_sponsor _ _ = False
--}

-- problem 6e
data InstagramUser = Influencer [String] [InstagramUser] | Normie

-- problem 6f
count_influencers :: InstagramUser -> Integer
count_influencers (Influencer _ followers) = toInteger $ length followers
count_influencers _ = 0

-- problem 7a
data LinkedList = EmptyList | ListNode Integer LinkedList
    deriving Show

ll_contains :: LinkedList -> Integer -> Bool
ll_contains EmptyList _ = False
ll_contains (ListNode x xs) target = if x == target
                                        then True
                                        else ll_contains xs target

-- problem 8b
longest_run :: [Bool] -> Int
longest_run lst = 

