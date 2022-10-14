# problem 1
from functools import reduce
def convert_to_decimal(bits):
    exponents = range(len(bits)-1, -1, -1)
    nums = [bit * 2**exp for bit, exp in zip(bits, exponents)]
    return reduce(lambda acc, num: acc + num, nums)

# problem 2a
# For each line in the lines list, split the line into 2 elements: the word
# and the number. Then, for each splitted element, create a tuple containing
# the word and the number.
def parse_csv(lines):
    return [(x[0], int(x[1]))
                for x in [line.split(',') for line in lines]]

# problem 2b
# Create a set containing each character of the sentence. Since sets contain
# only unique elements, duplicates will not be inserted.
def unique_characters(sentence):
    return {c for c in sentence}

# problem 2c
# Use range to generate numbers from lower_bound to upper_bound (inclusive). For
# each number x, create a mapping from x to x squared.
def squares_dict(lower_bound, upper_bound):
    return {x : x**2 for x in range(lower_bound, upper_bound + 1)}

# problem 3
# Join all elements of the list containing only characters in sentence that are
# not in chars_to_remove.
def strip_characters(sentence, chars_to_remove):
    return "".join([c for c in sentence if c not in chars_to_remove])

# problem 7a
def largest_sum(nums, k):
    if k < 0 or k > len(nums):
        raise ValueError
    elif k == 0:
        return 0
    max_sum = None
    for i in range(len(nums)-k):
        sum = 0
        for num in nums[i:i+k]: # iterate through k consecutive elements
            sum += num
        if max_sum is None or sum > max_sum: # update max_sum if necessary
            max_sum = sum
    return max_sum

# probelm 8a
class Event:
    def __init__(self, start_time, end_time):
        if start_time >= end_time:
            raise ValueError
        self.start_time, self.end_time = start_time, end_time

# event = Event(10, 20)
# print(f"Start: {event.start_time}, End: {event.end_time}")
# try:
#     invalid_event = Event(20, 10)
#     print("Success")
# except ValueError:
#     print("Created an invalid event")

# problem 8b
class Calendar:
    def __init__(self):
        self._events = []
    
    def get_events(self):
        return self._events
    
    def add_event(self, event):
        if (type(event) is not Event):
            raise TypeError
        self._events.append(event)
    
# calendar = Calendar()
# print(calendar.get_events())
# calendar.add_event(Event(10, 20))
# print(calendar.get_events()[0].start_time)
# try:
#     calendar.add_event("not an event")
# except TypeError:
#     print("Invalid event")

class AdventCalendar(Calendar):
    def __init__(self, year):
        self._events = []
        self.year = year

# advent_calendar = AdventCalendar(2022)
# print(advent_calendar.get_events())

# problem 9
def outer_function(x):
    def inner_function(y):
        return x * y
    return inner_function

func = outer_function(10)
print(func(20))