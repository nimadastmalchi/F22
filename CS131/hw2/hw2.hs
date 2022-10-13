-- problem 1a
-- Using partial application:
scale_nums :: [Integer] -> Integer -> [Integer]
scale_nums lst factor = map (* factor) lst

-- Using lambda closure:
scale_nums' :: [Integer] -> Integer -> [Integer]
scale_nums' lst factor = map (\x -> factor * x) lst

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

-- problem 6a
-- data InstagramUser = Influencer | Normie

-- problem 6b
-- lit_collab :: InstagramUser -> InstagramUser -> Bool
-- lit_collab Influencer Influencer = True
-- lit_collab _ _ = False

-- problem 6c
-- data InstagramUser = Influencer [String] | Normie

-- problem 6d
-- is_sponsor :: InstagramUser -> String -> Bool

-- -- If InstagramUser is Influencer, then return true if sponsor is in the user's sponsor list:
-- is_sponsor (Influencer lst) sponsor = elem sponsor lst
-- -- If InstagramUser is anything else, return False:
-- is_sponsor _ _ = False

-- problem 6e
data InstagramUser =
    Influencer
        [String]        -- sponsorships
        [InstagramUser] -- followers
  | Normie

-- problem 6f
-- helper function:
-- return True if InstagramUser is Influencer, False otherwise
is_influencer :: InstagramUser -> Bool
is_influencer (Influencer _ _) = True
is_influencer _ = False

count_influencers :: InstagramUser -> Integer
-- If InstagramUser is Influencer, filter out all of its non-influencer followers and
-- return the length:
count_influencers (Influencer _ followers) =
    toInteger $
    length $
    filter is_influencer followers
-- If InstagramUser is anything else, return 0:
count_influencers _ = 0

-- problem 7a
data LinkedList = EmptyList | ListNode Integer LinkedList
    deriving Show

ll_contains :: LinkedList -> Integer -> Bool
ll_contains EmptyList _ = False
ll_contains (ListNode x xs) target = if x == target
                                        then True
                                        else ll_contains xs target

-- problem 7b
-- parameters: index, new value, linked list
-- returns: new linked list with the inserted value
ll_insert :: Int -> Integer -> LinkedList -> LinkedList

-- problem 7c
ll_insert _ val EmptyList = ListNode val EmptyList
ll_insert ind val (ListNode x xs)
    | ind <= 0  = ListNode val (ListNode x xs)
    | otherwise = ListNode x (ll_insert (ind-1) val xs)

-- problem 8b
longest_run :: [Bool] -> Int
longest_run lst = snd $ foldr
    (\x acc -> let cur = fst acc
                   ans = snd acc
                in
                   if x then (cur+1, max (cur+1) ans)
                        else (0, ans)) (0, 0) lst



-- problem 8d
data Tree = Empty | Node Integer [Tree]
max_tree_value :: Tree -> Integer
max_tree_value Empty = 0
max_tree_value (Node val []) = val
max_tree_value (Node val children) =
    max val
        (foldr (\x acc -> max acc (max_tree_value x))
               0
               children)


-- problem 9
fib_array = 1 : 1 : zipWith (+) fib_array (tail fib_array)
fibonacci x = take x fib_array

-- problem 10
data Event = Travel Integer | Fight Integer | Heal Integer

process_event :: Event -> Integer -> Integer
process_event (Travel dist) health
    | health <= 40 = health
    | otherwise    = process_event (Heal (div dist 4)) health
process_event (Fight hitpts) health
    | health <= 40 = health - (div hitpts 2)
    | otherwise    = health - hitpts
process_event (Heal amt) health = min (health + amt) 100

super_giuseppe :: [Event] -> Integer
super_giuseppe events = (foldl
                           (\acc e -> if acc <= 0
                                        then -1
                                        else process_event e acc)
                           100
                           events)

