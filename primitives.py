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
def scheme_booleanQ(x):
    return scheme_true(x) or scheme_false(x)

def scheme_true(x):
    return x == '#t'

def scheme_false(x):
    return x == '#f'

@primitive("not")
def scheme_not(x):
    return '#t' if scheme_false(x) else '#f'

@primitive("and")
def scheme_and(x, y):
    return '#t' if x != '#f' and y != '#f' else '#f'

@primitive("or")
def scheme_or(x, y):
    return '#f' if x == '#f' and y == '#f' else '#t'

@primitive("equal?")
def scheme_eqQ(x, y):
    return x == y

@list_function("null?")
@primitive("null?")
def scheme_nullQ(x):
    return isinstance(x, list) and len(x) == 0

@list_function("list?")
@primitive("list?")
def scheme_listQ(x):
    return isinstance(x, list)

@list_function("length")
@primitive("length")
def scheme_length(x):
    return len(x)

@list_function("car")
@primitive("car")
def scheme_car(x):
    return x[0]

@list_function("cdr")
@primitive("cdr")
def scheme_cdr(x):
    return x[1:]

@list_function("cons")
@primitive("cons")
def scheme_cons(x, y):
    return [x, y]

@primitive("map")
def scheme_map(fn, args):
    res = []
    for arg in args:
        res.append(fn(arg))
    return res

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
def scheme_quo(x, y):
    return number(x) // number(y)

@primitive("remainder")
def scheme_rem(x, y):
    return number(x) % number(y)

@primitive("floor")
def scheme_floor(x):
    return number(x) // 1

@primitive("ceil")
def scheme_ceil(x):
    x = number(x)
    return x if x % 1 == 0 else x // 1 + 1

@primitive("=")
def scheme_eq(args):
    lastarg = number(args[0])
    for arg in args:
        if number(arg) != lastarg:
            return False
    return True

@primitive("<")
def scheme_lt(x, y):
    return number(x) < number(y)

@primitive(">")
def scheme_gt(x, y):
    return number(x) > number(y)

@primitive("<=")
def scheme_le(x, y):
    return number(x) <= number(y)

@primitive(">=")
def scheme_ge(x, y):
    return number(x) >= number(y)

@primitive("even?")
def scheme_evenQ(x):
    return number(x) % 2 == 0

@primitive("odd?")
def scheme_oddQ(x):
    return number(x) % 2 == 1

@primitive("zero?")
def scheme_zeroQ(x):
    return number(x) == 0