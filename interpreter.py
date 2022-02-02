import sys
from conditionals import CondBlock, IfBlock
import utils
import primitives
import lambdas

FUNCTIONS = primitives.FUNCTIONS
# Stores defined constant names as keys, their values as values
DEFINED_CONSTANTS = {}
# Stores function names as keys, lambda function objects as values
DEFINED_FUNCTIONS = {}
Line_Number = 1


# Executes the given function with the given arguments
def execute(func, args):
    # process all the commands within the command
    if (isinstance(func, lambdas.LambdaFunction)) or (func not in ['if', 'cond', 'define', 'lambda']):
        for i in range(len(args)):
            if utils.checkStartEnd(args[i]) == utils.CSE_EXECUTABLE_LIST:
                args[i] = processCommand(args[i])
            # turn into a nonexecutable list if we're just comparing
            if func == 'equal?' and isinstance(args[i], list):
                args[i] = utils.listTononexList(args[i])
    
    result = None

    if isinstance(func, lambdas.LambdaFunction):
        result = execute_lambda(func, args)
    else:
        # give different input to list functions
        if(func in primitives.LIST_FUNCTIONS):
            # single list
            if len(args) == 1:
                if utils.checkStartEnd(args[0]) in [utils.CSE_EXECUTABLE_LIST, utils.CSE_NONEXECUTABLE_LIST]:
                    args = utils.getListFromCommand(args[0])[1]
                    args = [args]
            # list of lists
            else:
                newArgs = []
                for arg in args:
                    newArgs.append(arg if utils.checkStartEnd(arg) == utils.CSE_OTHER else utils.getListFromCommand(arg)[1])
                args = newArgs

        result = None

        # call the corresponding lambda if the function is a defined function. call from the default functions otherwise
        if func in DEFINED_FUNCTIONS:
            result = execute_lambda(DEFINED_FUNCTIONS[func], args)
        else:
            try:
                result = FUNCTIONS[func](args)
            except KeyError:
                print("No declaration seen for \"" + str(func) + "\". Quitting.")
                sys.exit()
    
    if func in ["cdr", "cons", "append"]:
        result = utils.listTononexList(result)

    if result is not None and isinstance(result, str) and utils.checkStartEnd(result) in [utils.CSE_EXECUTABLE_LIST, utils.CSE_NONEXECUTABLE_LIST]:
        result = utils.fixWhitespace(result)

    return result

# Constructs an instance of lambda function class based on given lambda expression and returns it
def construct_lambda(args, body):
    toListFn = lambda comm : utils.getListFromCommand(comm)[1]
    lambdaFunction = lambdas.LambdaFunction(args, body, toListFn)
    return lambdaFunction

# Takes as input an instance of lambda function class and a list of arguments
# Plugs in the arguments and executes function
def execute_lambda(lambdaFunction, args):
    # make sure that the amount of arguments is correct
    primitives.exit_peacefully("<lambda function>", lambdaFunction.argCount, len(args))
    return processCommand(lambdaFunction.plug(args))

@primitives.primitive("lambda")
def scheme_lambda(args):
    return construct_lambda(args[0], args[1])

# Constructs an instance of if block class based on given arguments and returns it
def construct_if(all):
    condition = all[0]
    trueBlock = all[1]
    falseBlock = all[2]
    execFn = lambda x : x if (utils.checkStartEnd(x) == utils.CSE_OTHER) else processCommand(x)
    ifBlock = IfBlock(condition, trueBlock, falseBlock, execFn)
    return ifBlock

# Takes as input an instance of if block class
# Returns the result of executing the correct block from it
def execute_if(ifBlock):
    return ifBlock.execFn(ifBlock.getChosen())

@primitives.primitive("if")
def scheme_if(args):
    primitives.exit_peacefully("if", 3, len(args))
    ifBlock = construct_if(args)
    return execute_if(ifBlock)

# Takes as input all the arguments for the cond
# Constructs an instance of cond block class based on them and returns it 
def construct_cond(all):
    conditions = []
    blocks = []

    for i in range(len(all) - 1):
        pair = utils.getListFromCommand(all[i])[1]
        conditions.append(pair[0])
        blocks.append(pair[1])
    blocks.append(utils.getListFromCommand(all[len(all) - 1])[1][1])

    execFn = lambda x : x if (utils.checkStartEnd(x) == utils.CSE_OTHER) else processCommand(x)
    condBlock = CondBlock(conditions, blocks, execFn)
    return condBlock

# Takes as input an instance of a cond class
# Executes the correct block from it and returns the result
def execute_cond(condBlock):
    return condBlock.execFn(condBlock.getChosen())

@primitives.primitive("cond")
def scheme_cond(args):
    condBlock = construct_cond(args)
    return execute_cond(condBlock)

# Plug in the constants defined by the user into the command/list
def plug_constants(comm):
    for constant in DEFINED_CONSTANTS:
        comm = utils.replaceInList(constant, DEFINED_CONSTANTS[constant], comm)
    return comm

# Given a scheme list as a single line, get it as a python list and either execute it and return result 
# or return the unchanged scheme list itself
def processCommand(comm):
    comm = plug_constants(comm)
    cmnd = utils.getListFromCommand(comm)
    if cmnd[0]:     # if the command is to be executed
        # this has to be a lambda function
        if utils.checkStartEnd(cmnd[1][0]) == utils.CSE_EXECUTABLE_LIST:
            # list representing lambda function
            funcList = utils.getListFromCommand(cmnd[1][0])[1]
            # make sure it is lambda function indeed
            if funcList[0] != 'lambda':
                print("Attempt to call invalid type. Quitting")
                sys.exit()
            lambdaFunction = construct_lambda(funcList[1], funcList[2])
            # first argument _ the lambda function. second argument _ the list of arguments for the function.
            return execute(lambdaFunction, cmnd[1][1:])
        else:
            # first argument _ the function. second argument _ the list of arguments for the function.
            return execute(cmnd[1][0], cmnd[1][1:])
    else:
        return comm

@primitives.primitive("eval")
def scheme_eval(args):
    # remove leading ' from the list and process the command
    return processCommand(args[0][1:])

@primitives.primitive("apply")
def scheme_apply(args):
    # list of arguments
    if isinstance(args[1], str) and utils.checkStartEnd(args[1]) == utils.CSE_NONEXECUTABLE_LIST:
        actArgs = utils.getListFromCommand(args[1])[1]
    else:
        actArgs = args[1]
    # function to be applied to the arguments
    func = args[0]
    return execute(func, actArgs)

@primitives.primitive("map")
def scheme_map(args):
    func = args[0]
    # given arguments for the mapped function as scheme lists
    actArgs = args[1:]
    # list of lists to use the function on
    argLists = []
    for arg in actArgs:
        argList = utils.getListFromCommand(arg)
        # be sure that we're mapping function on a ready list
        if argList[0]:
            print("Invalid second argument for function \"map\". Quitting")
            sys.exit()
        argLists.append(argList[1])
    
    res = []

    for i in range(len(argLists[0])):
        # command to execute to get a single element in the to-be-returned list
        cmnd = []
        cmnd.append(func)
        for j in range(len(argLists)):
            cmnd.append(argLists[j][i])

        res.append(execute(cmnd[0], cmnd[1:]))
    
    return res

# Reads a command from stdin and returns it as one line with whitespace fixed
def getCommandFromStdin():
    global Line_Number
    comm = ''
    openBr = 0      # keep count of open brackets
    while True:
        print('#' + str(Line_Number) + ':scm:> ', end='')
        Line_Number += 1
        line = input() + ' '
        comm += line
        if line == ' ':
            continue
        for c in line:
            # check for open and closed brackets within the command
            if c == '(':
                openBr += 1
            elif c == ')':
                openBr -= 1
        # terminate program if more closed brackets than open ones
        if openBr < 0:
            print("Invalid input based on brackets. Quitting")
            sys.exit()
        # finish reading the command if all open brackets have been closed
        if openBr == 0:
            break
        
    return utils.fixWhitespace(utils.removeComments(comm))

# Reads the next command from a file and returns it as one line with whitespace fixed
def getCommandFromFile(file, lineCount):
    comm = ''
    openBr = 0      # keep count of open brackets
    while True:
        lineCount[0] += 1
        line = file.readline()
        comm += line
        # break the loop if no more lines to be read from file
        if not line:
            # terminate program if unclosed brackets
            if openBr != 0:
                print("Found unexpected EOF at line " + str(lineCount[0] - 1) + ". Quitting.")
                sys.exit()
            break
        for c in line:
            # check for open and closed brackets within the command
            if c == '(':
                openBr += 1
            elif c == ')':
                openBr -= 1
        # terminate program if more closed brackets than open ones
        if openBr < 0:
            print("Found invalid brackets at line " + str(lineCount[0]) + ". Quitting.")
            sys.exit()
        # finish reading the command if all open brackets have been closed
        if openBr == 0:
            break
    
    if comm == '':
        return None
    
    return utils.fixWhitespace(utils.removeComments(comm))

# Process all commands from the given file.
# Return 1 if there was a call to exit within the file, return 0 otherwise.
def processFile(filename):
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        print("Unable to find file \"" + filename + "\". Quitting")
        sys.exit()

    lineCount = [0]
    while True:
        comm = getCommandFromFile(file, lineCount)
        
        # stop reading if we reached EOF
        if comm is None:
            break

        # continue if the command was an empty line
        if comm == '':
            continue

        # make sure that the input command was a list
        if utils.checkStartEnd(comm) not in [utils.CSE_EXECUTABLE_LIST, utils.CSE_NONEXECUTABLE_LIST]:
            print("Found invalid input ending at line " + str(lineCount[0]) + ". Quitting")
            sys.exit()

        # stop reading if we got an exit command
        if comm == '(exit)':
            break

        # process the command that we read
        if comm:
            processCommand(comm)
    # close the file after reading from it
    file.close()

    if comm is None:            # return 0 if the program can go on
        return 0

    if comm == '(exit)':        # return 1 if the program ends in this file
        return 1

# Load a file, executing it line by line
@primitives.primitive("load")
def scheme_load(arg):
    filename = arg[0]
    if utils.checkStartEnd(filename) != utils.CSE_STRING:
        print("Invalid input for function \"load\". Make sure to use quotes.")
        return
    # Return from the program if there is an exit command in the file
    if processFile(filename[1:len(filename)-1]) == 1:
        sys.exit()
    else:
        return

# Used to print to console with a command
@primitives.primitive("display")
def scheme_display(args):
    utils.output(args[0])

# Puts a new line to the console
@primitives.primitive("newline")
def scheme_newline(args):
    print("")

# Defines a constant
def define_constant(arg, val):
    DEFINED_CONSTANTS[str(arg)] = str(val)

# Defines a function for later use
def define_function(arg, val):
    # first part of the function _ the name and the arguments passed
    face = utils.getListFromCommand(arg)[1]
    # the implementation of the function
    body = val
    name = face[0]
    # passed arguments
    args = utils.listToSchemeList(face[1:])
    lambdaFunction = construct_lambda(args, body)
    # keep the function in the defined functions dictionary by its name
    DEFINED_FUNCTIONS[name] = lambdaFunction

# Handles define command
@primitives.primitive("define")
def scheme_define(args):
    arg = args[0]
    val = args[1]
    if utils.checkStartEnd(arg) == utils.CSE_EXECUTABLE_LIST:
        define_function(arg, val)
    else:
        define_constant(arg, val)

# Keep processing commands from stdin.
def processStdin():
    while True:
        comm = getCommandFromStdin()
        
        # make sure that the input command was a list
        if utils.checkStartEnd(comm) not in [utils.CSE_EXECUTABLE_LIST, utils.CSE_NONEXECUTABLE_LIST]:
            print("Invalid input: input command must be a list. Quitting")
            sys.exit()

        # quit reading commands on (exit) command
        if comm == '(exit)':
            break

        result = processCommand(comm)
        
        utils.output(result)
        if result is not None:
            print('')

# Take a Y or N from the user. Used for confirmation
def takeYorN():
    inp = input()
    while len(inp) == 0 or (inp[0]).capitalize() not in ['Y', 'N']:
        inp = input()
    return inp[0]

# Update the recursion limit based on user input
def askRecursionLimit():
    default = sys.getrecursionlimit()
    chosen = input("Enter a new recursion limit: ")
    while not chosen.isnumeric():
        chosen = input("Invalid input. Try again: ")
    chosen = int(chosen)

    choice = True
    if chosen < default:
        print("The value you entered is less than the default. Are you sure?(Y/N) ", end="")
        choice = (takeYorN() == 'Y')
    elif chosen > 25 * default:
        print("The value you entered is more than " + str(chosen // default // 5 * 5) + " times greater than the default. Are you sure?(Y/N) ", end="")
        choice = (takeYorN() == 'Y')
    
    if choice:
        sys.setrecursionlimit(chosen)

# Processes the command line arguments provided to the interpreter.
# It is possible to provide a filename and an optional argument "reclim".
# reclim has to be the last argument. If you provide it, you get to choose a recursion limit.
# This function returns a list. 
# First element of list is 0 if we're opening the interpreter.
# It is 1 if we're running the interpreter through a file, with second element being the filename
def processCLA(CLA):
    # no arguments
    if len(CLA) == 0:
        return [0]
    # one argument
    if len(CLA) == 1:
        if CLA[0] == "reclim":
            askRecursionLimit()
            return [0]
        else:
            return [1, CLA[0]]
    # two arguments
    if len(CLA) == 2:
        if CLA[1] != "reclim":
            print("Unrecognized argument " + str(CLA[1]) + ", ignoring.")
        else:
            askRecursionLimit()
        return [1, CLA[0]]
    # too many arguments
    print('Too many command line arguments, opening the application the default way.')
    print('usage: python3 interpreter.py {optional: <filename> reclim}')
    return [0]
    
# Main function takes command-line arguments. 
# If the user wants to run a program from a file, then there should be a command-line argument: The name of the file.
# User can also set the recursion limit by entering "reclim" as the last argument.
# If there are too many(more than 2) arguments or no arguments, then the commands will be taken straight from stdin.
def main(args):
    way = processCLA(args)
    # process commands from stdin
    if way[0] == 0:
        processStdin()
    else:
        processFile(way[1])

if __name__ == '__main__':
    main(sys.argv[1:])
