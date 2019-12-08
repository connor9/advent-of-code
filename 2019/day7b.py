# --- Part Two ---
#
# It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the
# thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:
#
#       O-------O  O-------O  O-------O  O-------O  O-------O
# 0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
#    |  O-------O  O-------O  O-------O  O-------O  O-------O |
#    |                                                        |
#    '--------------------------------------------------------+
#                                                             |
#                                                             v
#                                                      (to thrusters)
#
# Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input,
# and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the
# feedback loop: the signal will be sent through the amplifiers many times.
#
# In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used
# exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce
# output many times before halting. Provide each amplifier its phase setting at its first input instruction; all
# further input/output instructions are for signals.
#
# Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue
# receiving and sending signals until it halts.
#
# All signals sent or received in this process will be between pairs of amplifiers except the very first signal and
# the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.
#
# Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens,
# the last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal
# that can be sent to the thrusters using the new phase settings and feedback loop arrangement.
#
# Here are some example programs:
#
#     Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):
#
#     3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
#     27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
#
#     Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):
#
#     3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
#     -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
#     53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10
#
# Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can
# be sent to the thrusters?
#


from .intcode import IntcodeComputer, parse_program, read_program
import itertools

if __name__ == '__main__':
    tests = [
        ('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5', [9, 8, 7, 6, 5], 139629729),
        (' 3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10', [9,7,8,5,6], 18216)
    ]

    for test in tests:
        instructions_data = parse_program(test[0])

        computers = []
        for i in range(0, 5):
            intcode = IntcodeComputer()
            intcode.load_memory(instructions_data)

            computers.append(intcode)

        seeds = tuple(zip(range(5), test[1]))

        # Pre-seed the initial phase for all the computers
        for seed in seeds:
            comp_index = seed[0]
            computers[comp_index].add_input(seed[1])
            computers[comp_index].run()

        output = 0

        step = 0
        while True:

            for i, comp in enumerate(computers):
                # signal_value
                print(i, "->", output)
                computers[i].add_input(output)
                computers[i].run()

                output = computers[i].get_output()
                print(i, "<-", output)
                # output = comp.get_outputs()

                step = step + 1

            if computers[4].halted == True:
                break

        print("Steps:", step)



    perms = list(itertools.permutations([5, 6, 7, 8, 9]))
    max = 0
    current_perm = None
    attempts = 0
    instructions_data = read_program("day7.txt")

    for perm in perms:

        computers = []
        for i in range(0, 5):
            intcode = IntcodeComputer()
            intcode.load_memory(instructions_data)

            computers.append(intcode)

        seeds = tuple(zip(range(5), perm))

        # Pre-seed the initial phase for all the computers
        for seed in seeds:
            comp_index = seed[0]
            computers[comp_index].add_input(seed[1])
            computers[comp_index].run()

        output = 0

        step = 0
        while True:

            for i, comp in enumerate(computers):
                # signal_value
                print(i, "->", output)
                computers[i].add_input(output)
                computers[i].run()

                output = computers[i].get_output()
                print(i, "<-", output)
                # output = comp.get_outputs()

                step = step + 1

            if computers[4].halted == True:
                break

        print("Steps:", step)
        print(output)
        if output > max:
            max = output
            current_perm = perm
        attempts = attempts + 1

    print(attempts)
    print(current_perm)
    print(max)