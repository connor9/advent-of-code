# --- Part Two ---
#
# During the second Go / No Go poll, the Elf in charge of the Rocket Equation Double-Checker stops the launch sequence.
# Apparently, you forgot to include additional fuel for the fuel you just added.
#
# Fuel itself requires fuel just like a module - take its mass, divide by three, round down, and subtract 2. However,
# that fuel also requires fuel, and that fuel requires fuel, and so on. Any mass that would require negative fuel should
# instead be treated as if it requires zero fuel; the remaining mass, if any, is instead handled by wishing really hard,
# which has no mass and is outside the scope of this calculation.
#
# So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated
# as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. For example:
#
#     A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0,
#     which would call for a negative fuel), so the total fuel required is still just 2.
#     At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then
#     requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the
#     total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
#     The fuel required by a module of mass 100756 and its fuel is:
#     33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
#
# What is the sum of the fuel requirements for all of the modules on your spacecraft when also taking into account the
# mass of the added fuel? (Calculate the fuel requirements for each module separately, then add them all up at the end.)

import math

# Parse input file as a list of integers
with open("day1.txt") as f:
    data = [int(i.replace("\n", "").strip()) for i in f.readlines()]


def calculate_mass_fuel(initial_mass):
    total_fuel_mass = 0
    current_fuel_mass = initial_mass
    while True:
        current_fuel_mass = math.floor((current_fuel_mass / 3)) - 2
        if current_fuel_mass <= 0:
            break
        total_fuel_mass = total_fuel_mass + current_fuel_mass

    return total_fuel_mass


# Verify test data
test_data = [12, 14, 1969, 100756]
results = [2, 2, 966, 50346]
expected_test_total = sum(results)
test_total = sum(calculate_mass_fuel(i) for i in test_data)

if expected_test_total != test_total:
    print("Test data doesn't add up. You've done something wrong. Good job!")
    import sys
    sys.exit(1)

# Calculate fuel required
output = [calculate_mass_fuel(i) for i in data]
total = sum(output)

print("Total fuel required", total)
