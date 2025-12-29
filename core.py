# this is here just to run the actuhall commands as needed.
# JUst for fun I'm making a sandbox CPU environment. Why not. I'll learn something maybe.
# Port this to C later... for fun xD
# FOR LATER: Make sure to check for reserver(-256) in all instructions.
# FOR LATER: Find a more elegant solution on how to handle strings instead of just writing bytes.
# Copyright 2025 Maciej Kaminski

import sys
mem = []

def TEST(address):
    if address < 0 or address >= len(mem):
        return 1
    elif mem[address] == -256:
        return 1
    else:
        return 0

def SET(type, address, data): # We set the data to a speciffic address to use later. 
    if TEST(address) == 1:
       return 1
    else:
        if type == "str":
            chars = []
            for char in data:
                chars.append(char)
            for i in range(len(chars)):
                mem[address + i] = chars[i]
            return 0
        if type == "byte":
            if data > 255:
                return 1
            elif data < -255:
                return 1
            else:
                mem[address] = data



def ADD(address_x, address_y):
    if TEST(address_x) == 1 or TEST(address_y) == 1:
        return 1
    else:
        if isinstance(mem[address_x], (int, float)) and isinstance(mem[address_y], (int, float)):
            mem[address_x] = mem[address_x] + mem[address_y]
            return mem[address_x]
        else:
            return 1

def OUT(address):
    if TEST(address) == 1:
        return 1
    else:
        print(f"{mem[address]}")
        return mem[address] 

def POP(address):
    if TEST(address) == 1:
        return 1
    else:
        mem[255] = mem[address]
        mem[address] = 0
        return mem[255]

def MOVE(address_x, address_y):
    if TEST(address_y) == 1 or TEST(address_x) == 1:
        return 1
    else:
        mem[address_y] = mem[address_x]
        mem[address_x] = 0
        return mem[address_y]
    
def DECR(address):
    if TEST(address) == 1:
        return 1
    else:
        if isinstance(mem[address], int) and mem[address] > 0:
            mem[address] = mem[address] - 1
            return mem[address]
        else:
            return 1

def NOTZ(address):
    if TEST(address) == 1:
        return 1
    else:
        if mem[address] > 0:
            return mem[address]
        elif mem[address] == 0:
            return 0

def POI(address, value=0):
    if TEST(address) == 1:
        return 1
    else:
        if value != 0:
            mem[address] = value
        else:
            return mem[address]

def ASSEMBLER(retro):
    with open(retro, 'r') as script:
        code = script.read().splitlines()
    for i in range(len(code)):
        code[i] = code[i].split(";", 1)[0].strip() #Strip Comments
    for i in range(len(code)):
        code[i] = code[i].split()
    code = [line for line in code if line]
    return code

def COMPILER(code):
    pc = 0
    while pc < len(code):
        instr = code[pc]
        operation = instr[0]
        raw_args = instr[1:]
        args = []
        for arg in raw_args:
            if arg.lstrip("-").isdigit():
                args.append(int(arg))
            else:
                args.append(arg)
        func = globals()[operation]
        result = func(*args)
        pc += 1

def main():
    for _ in range(64000):
        mem.append(0)
    if len(sys.argv) < 2:
        print("Usage: python3 core.py program.retro")
        return
    filename = sys.argv[1]
    program = ASSEMBLER(filename)
    COMPILER(program)

if __name__ == "__main__":
    main()
