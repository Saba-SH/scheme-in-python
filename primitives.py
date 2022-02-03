from sys import exit

# All of the functions here will be defined as soon as you start the program
FUNCTIONS = {}
LIST_FUNCTIONS = set()

def number(x):
    return int(x) if str(x).find('.') == -1 else float(x)

def list_function(name):
    def add(fn):
        LIST_FUNCTIONS.add(name)
        return fn
    return add

def primitive(name):
    def add(fn):
        FUNCTIONS[name] = fn
        return fn
    return add

def exit_peacefully(funcName, expected, got):
    if expected != got:
        print("Invalid argument count for function \"" + funcName + "\". Expected " + str(expected) + ", got "+ str(got) + ". Quitting.")
        exit()

@primitive("boolean?")
def scheme_booleanQ(args):
    exit_peacefully("boolean?", 1, len(args))
    x = args[0]
    return '#t' if (scheme_true(x) or scheme_false(x)) else '#f'

def scheme_true(x):
    return x == '#t'

def scheme_false(x):
    return x == '#f'

@primitive("not")
def scheme_not(args):
    exit_peacefully("not", 1, len(args))
    x = args[0]
    return '#t' if scheme_false(x) else '#f'

@primitive("and")
def scheme_and(args):
    # return false if false is to be found in the arguments
    # return the last non-boolean if one exists. return true otherwise
    # "and" works like this in scheme for some reason
    for arg in args:
        if scheme_false(arg):
            return '#f'
        
    for arg in reversed(args):
        if not scheme_booleanQ([arg]):
            return arg
    
    return '#t'

@primitive("or")
def scheme_or(args):
    # return true if true is to be found in the arguments
    # return the first non-boolean if one exists. return false otherwise
    # "or" works like this in scheme for some reason
    for arg in args:
        if scheme_true(arg):
            return '#t'
    
    for arg in args:
        if not scheme_false(arg):
            return arg

    return '#f'

@primitive("equal?")
def scheme_eqQ(args):
    exit_peacefully("equal?", 2, len(args))
    return '#t' if str(args[0]) == str(args[1]) else '#f'

@list_function("null?")
@primitive("null?")
def scheme_nullQ(args):
    exit_peacefully("null?", 1, len(args))
    return '#t' if isinstance(args[0], list) and len(args[0]) == 0 else '#f'

@list_function("list?")
@primitive("list?")
def scheme_listQ(args):
    exit_peacefully("list?", 1, len(args))
    return '#t' if isinstance(args[0], list) else '#f'

@list_function("length")
@primitive("length")
def scheme_length(args):
    exit_peacefully("length", 1, len(args))
    return len(args[0])

@list_function("car")
@primitive("car")
def scheme_car(args):
    return args[0][0]

@list_function("cdr")
@primitive("cdr")
def scheme_cdr(args):
    return args[0][1:]

@list_function("cons")
@primitive("cons")
def scheme_cons(args):
    exit_peacefully("cons", 2, len(args))
    res = [args[0]]
    if isinstance(args[1], list):
        for elem in args[1]:
            res.append(elem)
    else:
        res.append(args[1])
    
    return res

@list_function("append")
@primitive("append")
def scheme_append(args):
    res = []
    for arg in args:
        res = res + arg
    return res

@primitive("quote")
def scheme_quote(args):
    exit_peacefully("quote", 1, len(args))
    return '\'' + args[0]

@primitive("list")
def scheme_list(args):
    return args

@primitive("string?")
def scheme_stringQ(args):
    exit_peacefully("string?", 1, len(args))
    elem = args[0]
    return '#t' if len(elem) >= 2 and [elem[0], elem[len(elem) - 1]] in [['\'', '\''], ['\"', '\"']] else '#f'

@primitive("number?")
def scheme_numberQ(args):
    exit_peacefully("number?", 1, len(args))
    elem = str(args[0])
    if elem.count('.') <= 1:
        occ = elem.find('.')
        if elem.find('-') > occ % len(elem):
            return '#f'
        if occ < len(elem) - 1:
            if scheme_integerQ([elem] if occ == -1 else [elem[0:occ] + elem[occ + 1:]]) == '#t':
                return '#t'
    return '#f'

@primitive("integer?")
def scheme_integerQ(args):
    exit_peacefully("integer?", 1, len(args))
    return '#t' if (args[0].isnumeric() or (args[0][0] == '-' and args[0][1:].isnumeric())) else '#f'

@primitive("+")
def scheme_add(args):
    res = 0
    for arg in args:
        res += number(arg)
    return res

@primitive("-")
def scheme_sub(args):
    if len(args) == 0:
        exit_peacefully("-", "at least 1", 0)
    if len(args) == 1:
        return -number(args[0])
    res = number(args[0])
    for arg in args[1:]:
        res -= number(arg)
    return res

@primitive("*")
def scheme_mul(args):
    res = 1
    for arg in args:
        res = res * number(arg)
    return res

@primitive("/")
def scheme_div(args):
    if len(args) == 0:
        exit_peacefully("/", "at least 1", 0)
    if len(args) == 1:
        return number(1 / number(args[0]))
    res = number(args[0])
    for arg in args[1:]:
        res = res / number(arg)
    return res

@primitive("quotient")
def scheme_quo(args):
    exit_peacefully("quotient", 2, len(args))
    return number(args[0]) // number(args[1])

@primitive("mod")
@primitive("remainder")
def scheme_rem(args):
    exit_peacefully("remainder", 2, len(args))
    return number(args[0]) % number(args[1])

@primitive("floor")
def scheme_floor(args):
    exit_peacefully("floor", 1, len(args))
    return number(args[0]) // 1

@primitive("ceil")
def scheme_ceil(args):
    exit_peacefully("ceil", 1, len(args))
    x = number(args[0])
    return x if x % 1 == 0 else x // 1 + 1

@primitive("max")
def scheme_max(args):
    return max(args)

@primitive("min")
def scheme_min(args):
    return min(args)

@primitive("=")
def scheme_eq(args):
    if len(args) == 0:
        exit_peacefully("=", "at least 1", 0)
    lastarg = number(args[0])
    for arg in args:
        if number(arg) != lastarg:
            return '#f'
    return '#t'

@primitive("<")
def scheme_lt(args):
    if len(args) == 0:
        exit_peacefully("<", "at least 1", 0)
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) >= number(args[i + 1]):
            return '#f'
    return '#t'

@primitive(">")
def scheme_gt(args):
    if len(args) == 0:
        exit_peacefully(">", "at least 1", 0)
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) <= number(args[i + 1]):
            return '#f'
    return '#t'

@primitive("<=")
def scheme_le(args):
    if len(args) == 0:
        exit_peacefully("<=", "at least 1", 0)
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) > number(args[i + 1]):
            return '#f'
    return '#t'

@primitive(">=")
def scheme_ge(args):
    if len(args) == 0:
        exit_peacefully(">=", "at least 1", 0)
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) < number(args[i + 1]):
            return '#f'
    return '#t'

@primitive("even?")
def scheme_evenQ(args):
    exit_peacefully("even?", 1, len(args))
    return '#t' if number(args[0]) % 2 == 0 else '#f'

@primitive("odd?")
def scheme_oddQ(args):
    exit_peacefully("odd?", 1, len(args))
    return '#t' if number(args[0]) % 2 == 1 else '#f'

@primitive("zero?")
def scheme_zeroQ(args):
    exit_peacefully("zero?", 1, len(args))
    return '#t' if number(args[0]) == 0 else '#f'
