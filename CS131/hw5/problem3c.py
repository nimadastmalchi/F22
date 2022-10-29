class X:
    def __init__(self):
        self.x = 2
x = X()
def func(x):
    x.x = 5
func(x)
print(x.x)
