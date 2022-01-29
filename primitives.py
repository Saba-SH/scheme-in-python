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

@primitive("boolean?")
def scheme_booleanQ(args):
    assert len(args) == 1
    x = args[0]
    return '#t' if (scheme_true(x) or scheme_false(x)) else '#f'

def scheme_true(x):
    return x == '#t'

def scheme_false(x):
    return x == '#f'

@primitive("not")
def scheme_not(args):
    assert len(args) == 1
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
    assert len(args) == 2
    return '#t' if args[0] == args[1] else '#f'

@list_function("null?")
@primitive("null?")
def scheme_nullQ(args):
    assert len(args) == 1
    return '#t' if isinstance(args[0][0], list) and len(args[0][0]) == 0 else '#f'

@list_function("list?")
@primitive("list?")
def scheme_listQ(args):
    assert len(args) == 1
    return '#t' if isinstance(args[0][0], list) else '#f'

@list_function("length")
@primitive("length")
def scheme_length(args):
    assert len(args) == 1
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
    assert len(args) == 2
    res = [args[0]]
    if isinstance(args[1], list):
        for elem in args[1]:
            res += elem
    else:
        res += args[1]
    
    return res

@list_function("append")
@primitive("append")
def scheme_append(args):
    res = []
    for arg in args:
        res = res + arg
    return res

@primitive("list")
def scheme_list(args):
    return args

# @primitive("string?")
# def scheme_stringQ(x):
#     return isinstance(x, str) and x.startswith('"')

# @primitive("number?")
# def scheme_numberQ(x):
#     return isinstance(x, int) or isinstance(x, float)

# @primitive("integer?")
# def scheme_integerQ(x):
#     return isinstance(x, int) or (scheme_numberQ(x) and round(x) == x)

@primitive("+")
def scheme_add(args):
    res = 0
    for arg in args:
        res += number(arg)
    return res

@primitive("-")
def scheme_sub(args):
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
    if len(args) == 1:
        return number(1 / number(args[0]))
    res = number(args[0])
    for arg in args[1:]:
        res = res / number(arg)
    return res

@primitive("quotient")
def scheme_quo(args):
    assert len(args) == 2
    return number(args[0]) // number(args[1])

@primitive("remainder")
def scheme_rem(args):
    assert len(args) == 2
    return number(args[0]) % number(args[1])

@primitive("floor")
def scheme_floor(args):
    assert len(args) == 1
    return number(args[0]) // 1

@primitive("ceil")
def scheme_ceil(args):
    assert len(args) == 1
    x = number(args[0])
    return x if x % 1 == 0 else x // 1 + 1

@primitive("=")
def scheme_eq(args):
    assert len(args) > 0
    lastarg = number(args[0])
    for arg in args:
        if number(arg) != lastarg:
            return '#f'
    return '#t'

@primitive("<")
def scheme_lt(args):
    assert len(args) > 0
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) >= number(args[i + 1]):
            return '#f'
    return '#t'

@primitive(">")
def scheme_gt(args):
    assert len(args) > 0
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) <= number(args[i + 1]):
            return '#f'
    return '#t'

@primitive("<=")
def scheme_le(args):
    assert len(args) > 0
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) > number(args[i + 1]):
            return '#f'
    return '#t'

@primitive(">=")
def scheme_ge(args):
    assert len(args) > 0
    if len(args) == 1:
        return '#t'
    for i in range(len(args) - 1):
        if number(args[i]) < number(args[i + 1]):
            return '#f'
    return '#t'

@primitive("even?")
def scheme_evenQ(args):
    assert len(args) == 1
    return '#t' if number(args[0]) % 2 == 0 else '#f'

@primitive("odd?")
def scheme_oddQ(args):
    assert len(args) == 1
    return '#t' if number(args[0]) % 2 == 1 else '#f'

@primitive("zero?")
def scheme_zeroQ(args):
    assert len(args) == 1
    return '#t' if number(args[0]) == 0 else '#f'