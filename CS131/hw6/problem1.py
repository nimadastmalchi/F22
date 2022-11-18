def foo(a):
    # a = 1
    a = 3 # a binds to value 3
    # copy value of a (3) into bar's first parameter.
    # copy result of baz() (5) into bar's second parameter
    bar(a, baz())
def bar(a, b):
    # a = 3, b = 5
    print("bar") # 2. print "bar"
    a = a + 1 # increment a by 1 to get 4
def baz():
    print("baz") # 1. print "baz"
    return 5
a = 1
foo(a) # copy value 1 into the parameter of foo
print(a) # 3. print "1"


def foo(a):
    # a refers to global variable a
    a = 3 # global variable a now holds 3
    bar(a, baz())
def bar(a, b):
    # a refers to global variable a (which currently holds 3)
    # b holds 5
    print("bar") # 2. print "bar"
    # increment global variable a to 4
    a = a + 1
def baz():
    print("baz") # 1. print "baz"
    return 5
a = 1
foo(a)
print(a) # 3. print "4"


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


def foo(a):
    # a points to thunk(1)
    a = 3 # a now points to thunk(3)
    bar(a, baz())
def bar(a, b):
    # a points to thunk(3)
    # b points to thunk(baz())
    print("bar") # 1. print "bar"
    a = a + 1 # a points to thunk(thunk(3) + 1)
def baz():
    print("baz")
    return 5
a = 1 # a points to thunk(1)
foo(a)
print(a) # evaluate thunk(1), which is 1
# 2. print "1"