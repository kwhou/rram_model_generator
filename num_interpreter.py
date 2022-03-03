
def num_interpreter(string):
    if not string[-1] in '0123456789.':
        if string[-1] == 'K':
            out = float(string[0:-1]) * 1e3
        elif string[-1] == 'm':
            out = float(string[0:-1]) * 1e-3
        elif string[-1] == 'u':
            out = float(string[0:-1]) * 1e-6
        elif string[-1] == 'n':
            out = float(string[0:-1]) * 1e-9
        elif string[-1] == 'p':
            out = float(string[0:-1]) * 1e-12
        elif string[-1] == 'f':
            out = float(string[0:-1]) * 1e-15
        elif string[-1] == 'a':
            out = float(string[0:-1]) * 1e-18
        else:
            print("Error: unit is undefined: " + string)
            exit()
    else:
        out = float(string)
    return out
