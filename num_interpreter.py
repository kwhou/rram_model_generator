# Copyright (c) 2022 Kuan-Wei Hou
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================

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
