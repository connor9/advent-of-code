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
# Your puzzle input is 231832-767346.

range_start = 231832
range_finish = 767346

tests = [
    "asdfasdf",
    111111,
    "111111",
    223450,
    "223450",
    123789,
    "123789",
    "asdfasdf",
    "112233",
    "123444",
    "111122"

]


def is_valid(password):
    if len(str(password)) != 6 or not str(password).isnumeric():
        return False

    password = str(password)

    prev_digit = -1

    double_count = 0
    has_double = False

    for digit in password:
        digit = int(digit)
        if(digit < prev_digit):
            return False
        if digit == prev_digit:
            double_count = double_count + 1
        else:
            if double_count == 1:
                has_double = True
            double_count = 0

        prev_digit = digit

    if double_count == 1:
        has_double = True

    if not has_double:
        return False

    return True

for test in tests:
    print(test, is_valid(test))

total = 0
for i in range(range_start, range_finish+1):

    if is_valid(i):
        total = total + 1

print(total)