
def remove_invalid_emails(inputs):
    return list(filter(lambda x : '@' in x and '.' in x and x.index('@') < x.index('.'), inputs))

print(remove_invalid_emails(["matt@matthewwang.me", "notreal", "stay@home", "st.ay@home"]))


from functools import reduce

def count_edu_emails(inputs):
  valid_emails = remove_invalid_emails(inputs)
  return reduce(lambda accum, current: accum + 1 if current[-3:] == "edu" else accum, valid_emails, 0)


print(count_edu_emails(["matt@matthewwang.me", "tree@stanford.edu", "beaver@mit.edu", "thisisntreallyan@edu.email"]))

def generate_email_validator(predicate):
    def func(lst):
        return list(filter(predicate, lst))
    return func

bad_validator = generate_email_validator(lambda x: len(x) > 3)
print(bad_validator(["a", "thisissonotanemail", "matt@matthewwang.me"]))


def compare_validators(inputs, predicates):
    return [len(list(filter(predicates[i], inputs))) for i in range(len(predicates))]

print(compare_validators(["matt@matthewwang.me", "makarlATucd.edu", "a@a.a"], [lambda x: len(x) > 3, lambda x: x != "makarlATucd.edu"]))

def fizzbuzz_list(start, end):
    return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else i for i in range(start, end + 1)]

print(fizzbuzz_list(10,15))

