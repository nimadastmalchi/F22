def foo(a):
   # local var a points to object int(1)
   a = 3 # local var a points to object int(3)
   bar(a, baz())
def bar(a, b):
   # local var a points to object int(3)
   # local var b points to object int(5)
   print("bar") # 2. print "bar"
   a = a + 1 # local var a poitns to object int(4)
def baz():
   print("baz") # 1. print "baz"
   return 5
a = 1 # a points to object int(1)
foo(a)
print(a) # 3. print "1"
