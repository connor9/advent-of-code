# --- Day 4: Secure Container ---
#
# You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the
# password on a sticky note, but someone threw it out.
#
# However, they do remember a few key facts about the password:
#
# It is a six-digit number. The value is within the range given in your puzzle input. Two adjacent digits are the
# same (like 22 in 122345). Going from left to right, the digits never decrease; they only ever increase or stay the
# same (like 111123 or 135679).
#
# Other than the range rule, the following are true:
#
#     111111 meets these criteria (double 11, never decreases).
#     223450 does not meet these criteria (decreasing pair of digits 50).
#     123789 does not meet these criteria (no double).
#
# How many different passwords within the range given in your puzzle input meet these criteria?
#
# Your puzzle input is 231832-767346.
#
# --- Part Two ---
#
# An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.
#
# Given this additional criterion, but still ignoring the range rule, the following are now true:
#
#     112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
#     123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
#     111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
#
# How many different passwords within the range given in your puzzle input meet all of the criteria?

range_start = 231832
range_finish = 767346


def is_valid(password):
    if len(str(password)) != 6 or not str(password).isnumeric():
        return False

    password = str(password)

    prev_digit = -1
    has_double = False
    for digit in password:
        digit = int(digit)
        if(digit < prev_digit):
            return False
        if digit == prev_digit:
            has_double = True
        prev_digit = digit

    if not has_double:
        return False

    return True

tests = [
    "asdfasdf",
    111111,
    "111111",
    223450,
    "223450",
    123789,
    "123789"
]

for test in tests:
    print(test, is_valid(test))

total = 0
for i in range(range_start, range_finish+1):

    if is_valid(i):
        total = total + 1

print(total)