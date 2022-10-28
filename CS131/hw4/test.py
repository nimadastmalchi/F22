from math import sqrt
def nth_fibonacci(n):
   phi = (1 + sqrt(5))/2
   psi = (1 - sqrt(5))/2
   return (phi**n - psi**n)/sqrt(5)
