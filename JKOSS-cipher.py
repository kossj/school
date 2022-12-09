def shift(c: str, s: int):  # Takes input of alpha or space char
    if c.isspace():
        return c  # If space, simply return
    elif c.islower():
        case = list(range(97, 123))  # Lowercase ASCII codes
    elif c.isupper():
        case = list(range(65, 91))  # Upper ASCII codes
    else:
        return TypeError
    return chr(case[(ord(c)+s-min(case)) % len(case)])  # If case is accessed before assignment, invalid char input


def caesar(instr: str, code: int):  # Confirms string compatibility, and runs through shift function
    if all(let.isalpha() or let.isspace() for let in instr):  # If string consists of alpha and spaces
        return ''.join(shift(let, code) for let in instr)  # Concatenate each result of the shift for each letter


if __name__ == '__main__':
    # a, b = input().split(sep=':')  # Place string and desired shift on same line, split with colon
    # if isinstance(b, int):  # Will not give a return if there are any errors in input
    #     print(caesar(a, int(b)))
    print(caesar("The Quick Brown Fox Jumps Over The Lazy Dog", 3))