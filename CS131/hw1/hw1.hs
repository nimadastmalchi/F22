-- Nima Amir Dastmalchi
-- 505320372
-- UCLA CS 131
-- Homework 1

-------------------------------------------------------------------------------

-- Problem 1
largest :: String -> String -> String
largest str1 str2 = if (length str1) >= (length str2)
                    then str1
                    else str2

-------------------------------------------------------------------------------

-- Problem 2
reflect :: Integer -> Integer
reflect 0 = 0
reflect num
    | num < 0 = (-1) + reflect (num+1)
    | num > 0 = 1 + reflect (num-1)

-------------------------------------------------------------------------------

-- Problem 3a
all_factors :: Integer -> [Integer]
all_factors num = [x | x <- [1..num], mod num x == 0]

-- Problem 3b
perfect_numbers :: [Integer]
perfect_numbers = [x | x <- [1..], x == (sum $ init $ all_factors x)]

-------------------------------------------------------------------------------

-- Problem 4
-- version 1 - if/else statement
is_even :: Integer -> Bool
is_even x = if x == 0
            then True
            else is_odd (x - 1)

is_odd :: Integer -> Bool
is_odd x = if x == 0
           then False
           else is_even (x - 1)

-- version 2 - guards
is_even' :: Integer -> Bool
is_even' x
    | x == 0    = True
    | otherwise = is_odd' (x - 1)

is_odd' x
    | x == 0    = False
    | otherwise = is_even' (x - 1)

-- version 3 - pattern matching
is_even'' :: Integer -> Bool
is_even'' 0 = True
is_even'' x = is_odd'' (x - 1)

is_odd'' :: Integer -> Bool
is_odd'' 0 = False
is_odd'' x = is_even'' (x - 1)

-------------------------------------------------------------------------------

-- Problem 5
count_occurrences :: (Eq a) => [a] -> [a] -> Integer
count_occurrences [] a2 = 1
count_occurrences a1 [] = 0
count_occurrences (x : xs) (y : ys)
    | x == y    = (count_occurrences xs ys) + (count_occurrences (x : xs) ys)
    | otherwise = count_occurrences (x : xs) ys
