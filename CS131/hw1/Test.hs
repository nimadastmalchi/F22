-- How to use this Test suite
-- name the file with your function implementations HW1.hs and place Test.hs in the same directory as HW1.hs
-- include the following as the first line of HW1.hs
--      module HW1 where
-- run ghci in your command line
-- run `:load Test.hs` in ghci
-- run `main` in ghci

import HW1

empty = ""
one_char = "a"
one_char2 = "b"
two_char = "bb"
empty_list = [] :: [Integer]

main::IO()
main = do
  (putStrLn (unwords ["\nTesting (", "largest", (show empty), (show empty), ")"]))
  (putStrLn ("Result: " ++ (show (largest empty empty))))
  (putStrLn ("Expect: " ++ (show empty)))

  (putStrLn (unwords ["\nTesting (", "largest", (show one_char), (show one_char2), ")"]))
  (putStrLn ("Result: " ++ (show (largest one_char one_char2))))
  (putStrLn ("Expect: " ++ (show one_char)))

  (putStrLn (unwords ["\nTesting (", "largest", (show one_char), (show two_char), ")"]))
  (putStrLn ("Result: " ++ (show (largest one_char two_char))))
  (putStrLn ("Expect: " ++ (show two_char)))

  (putStrLn (unwords ["\nTesting (", "largest", (show two_char), (show one_char), ")"]))
  (putStrLn ("Result: " ++ (show (largest two_char one_char))))
  (putStrLn ("Expect: " ++ (show two_char)))

  (putStrLn (unwords ["\nTesting (", "all_factors", (show 0), ")"]))
  (putStrLn ("Result: " ++ (show (all_factors 0))))
  (putStrLn ("Expect: " ++ (show [0])))

  (putStrLn (unwords ["\nTesting (", "all_factors", (show 1), ")"]))
  (putStrLn ("Result: " ++ (show (all_factors 1))))
  (putStrLn ("Expect: " ++ (show [1])))

  (putStrLn (unwords ["\nTesting (", "all_factors", (show 2), ")"]))
  (putStrLn ("Result: " ++ (show (all_factors 2))))
  (putStrLn ("Expect: " ++ (show [1,2])))

  (putStrLn (unwords ["\nTesting (", "all_factors", (show 3), ")"]))
  (putStrLn ("Result: " ++ (show (all_factors 3))))
  (putStrLn ("Expect: " ++ (show [1,3])))

  (putStrLn (unwords ["\nTesting (", "all_factors", (show 4), ")"]))
  (putStrLn ("Result: " ++ (show (all_factors 4))))
  (putStrLn ("Expect: " ++ (show [1,2,4])))

  (putStrLn (unwords ["\nTesting (", "all_factors", (show 12), ")"]))
  (putStrLn ("Result: " ++ (show (all_factors 12))))
  (putStrLn ("Expect: " ++ (show [1,2,3,4,6,12])))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show empty_list), (show empty_list), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences empty_list empty_list))))
  (putStrLn ("Expect: " ++ (show 1)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show empty_list), (show [10, 50, 40, 20, 50, 40, 30]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [] [10, 50, 40, 20, 50, 40, 30]))))
  (putStrLn ("Expect: " ++ (show 1)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [10]), (show empty_list), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [10] []))))
  (putStrLn ("Expect: " ++ (show 0)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [10]), (show [10]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [10] [10]))))
  (putStrLn ("Expect: " ++ (show 1)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [10]), (show [10, 10]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [10] [10, 10]))))
  (putStrLn ("Expect: " ++ (show 2)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [10, 20, 40]), (show [10, 50, 40, 20, 50, 40, 30]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [10, 20, 40] [10, 50, 40, 20, 50, 40, 30]))))
  (putStrLn ("Expect: " ++ (show 1)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [10, 40, 30]), (show [10, 50, 40, 20, 50, 40, 30]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [10, 40, 30] [10, 50, 40, 20, 50, 40, 30]))))
  (putStrLn ("Expect: " ++ (show 2)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [20, 10, 40]), (show [10, 50, 40, 20, 50, 40, 30]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [20, 10, 40] [10, 50, 40, 20, 50, 40, 30]))))
  (putStrLn ("Expect: " ++ (show 0)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [50, 40, 30]), (show [10, 50, 40, 20, 50, 40, 30]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [50, 40, 30] [10, 50, 40, 20, 50, 40, 30]))))
  (putStrLn ("Expect: " ++ (show 3)))

  (putStrLn (unwords ["\nTesting (", "count_occurrences", (show [10, 50, 40, 20, 50, 40, 30]), (show [10, 50, 40, 20, 50, 40, 30]), ")"]))
  (putStrLn ("Result: " ++ (show (count_occurrences [10, 50, 40, 20, 50, 40, 30] [10, 50, 40, 20, 50, 40, 30]))))
  (putStrLn ("Expect: " ++ (show 1)))


