from .intcode_v3 import IntcodeComputer, parse_program, read_program

tests = [
    ['109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99', [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], 'takes no input and produces a copy of itself as output.'],
    ['1102,34915192,34915192,7,4,7,99,0', [1219070632396864], 'should output a 16-digit number.'],
    ['104,1125899906842624,99', [1125899906842624], 'should output the large number in the middle.']
]

for test in tests:
    instructions_data = parse_program(test[0])

    intcode = IntcodeComputer()
    intcode.load_memory(instructions_data)
    intcode.run()

    print("out:", intcode.outputs)
    if intcode.outputs == test[1]:
        print("PASS")
    else:
        print("FAIL")


# Real program

instructions_data = read_program("day9.txt")
intcode = IntcodeComputer()
intcode.load_memory(instructions_data)
intcode.add_input(1)
intcode.run()



