if (e() || f() && g() || h())
    do_something();
if (e() && f() || g() && h())
    do_something();
if (e() && (f() || g())
    do_something();


# First if statement:
if (e())
    do_something()
else if (f())
    if (g())
        do_something()
else if (h())
    do_something()

# Second if statement:
if (e())
    if (f())
        do_something()
else if (g())
    if (h())
        do_something()

# Third if statement:
if (e())
    if (f())
        do_something()
    else if (g())
        do_something()


