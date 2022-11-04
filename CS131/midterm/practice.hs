dedup :: [Int] -> [Int]
dedup [] = []
dedup (x:xs) = dedupAux xs x [x]

dedupAux :: [Int] -> Int -> [Int] -> [Int]
dedupAux [] y acc = acc
dedupAux (x:xs) y acc 
    | x == y = dedupAux xs y acc
    | x /= y = dedupAux xs x (acc ++ [x])


foo :: Int -> Int -> (Int -> (Int -> Int))

foo x = \y -> \q -> \r -> q + r + x + y

q :: Int -> (Int -> (Int -> Int)
