longest_run lst  = snd (foldl (\acc cur -> if cur == True then (fst acc + 1, max (fst acc + 1) (snd acc)) else (0, snd acc)) (0, 0) lst)

