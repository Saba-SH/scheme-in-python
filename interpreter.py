import sys
import primitives
import lambdas

FUNCTIONS = primitives.FUNCTIONS
# Stores defined constant names as keys, their values as values
DEFINED_CONSTANTS = {}
# Stores function names as keys, lambda function objects as values
DEFINED_FUNCTIONS = {}
Line_Number = 1

# Gets rid of extra whitespace.
# Returns the given command as being on one line, 
# only whitespace being single spaces between lists and elements of lists.
def fixWhitespace(comm):
    comm = comm.replace('\n', ' ')
    comm = ' '.join(comm.split())
    comm = comm.replace('( ', '(')
    comm = comm.replace(' )', ')')
    comm = comm.replace('\' ', '\'')
    return comm

# Checks the start and end of string.
# If it's like (...), return 0
# If it's like '(...), return 1
# If it's like '...' or "...", return 2
# Return 3 otherwise
def checkStartEnd(strn):
    if strn[len(strn) - 1] == ')' and strn[0] == '(':
        return 0
    if strn[len(strn) - 1] == ')' and strn[0:2] == '\'(':
        return 1
    if [strn[0], strn[len(strn) - 1]] in [['\'', '\''], ['\"', '\"']]:
        return 2
    return 3

# Returns the first occurence after pos of a substring in strn being encased between leftC and rightC.
# leftC and rightC are included in the result
# leftC and rightC should be different
def getEncasedIn(strn, pos, leftC, rightC):
    if leftC == rightC:
        return ""
        
    stepL = len(leftC)
    stepR = len(rightC)

    # Get to the closest occurence of leftC
    startPos = strn.find(leftC, pos)
    pos = startPos

    leftCount = 0
    
    while pos < len(strn):
        if strn[pos:(pos + stepL)] == leftC:        # skip step characters if encountered leftC or rightC
            leftCount += 1
            pos += stepL
        elif strn[pos:(pos + stepR)] == rightC:
            leftCount -= 1
            pos += stepR
        else:                                       # skip only one character if encountered neither
            pos += 1
        
        if leftCount == 0:                          # return the desired substring if we found it
            return strn[startPos:pos]

    return ''                                       # return empty string if we got to the end of strn
        
# Returns the given command as a list. Assumes that the command is properly structured.
# First element of the returned list is whether the list should be evaluated, 
# second element is the list of the list's elements
def getListFromCommand(comm):
    res = []
    comm = comm[:len(comm) - 1]         # remove bracket at the end
    if comm[0] == '\'':                 # remove '( at the start
        comm = comm[2:]
        res.append(False)
    else:                               # remove ( at the start
        res.append(True)
        comm = comm[1:]
    
    elems = []
    pos = 0

    while pos < len(comm):
        if comm[pos] == '(':          # executable list
            newElem = getEncasedIn(comm, pos, '(', ')')
        elif (pos < len(comm) - 1) and comm[pos:pos + 2] == '\'(':           # non-executable list
            newElem = getEncasedIn(comm, pos, '\'(', ')')
        else:                           # just an element
            beforeNext = comm.find(' ', pos)
            if beforeNext == -1:
                beforeNext = len(comm)
            newElem = comm[pos:beforeNext]

        # append the new element and move the position forward
        elems.append(newElem)
        pos += len(newElem)
        pos += 1

    res.append(elems)
    # print(res)                         ###############################################
    return res

# Returns a string representation of the given python list
def listToSchemeList(lst):
    res = '('
    if len(lst) > 0:
        res += listToSchemeList(lst[0]) if isinstance(lst[0], list) else str(lst[0])
    for elem in lst[1:]:
        res += ' ' + (listToSchemeList(elem) if isinstance(elem, list) else str(elem))
    res += ')'
    return res

# Executes the given function with the given arguments
def execute(func, args):
    if (isinstance(func, lambdas.LambdaFunction)) or (func not in ['define', 'lambda']):
        for i in range(len(args)):
            if checkStartEnd(args[i]) == 0:
                args[i] = processCommand(args[i])
    
    result = None

    if isinstance(func, lambdas.LambdaFunction):
        result = execute_lambda(func, args)
    else:
        if(func in primitives.LIST_FUNCTIONS):
            if len(args) == 1:
                args = getListFromCommand(args[0])[1]
            else:
                newArgs = []
                for arg in args:
                    newArgs.append(getListFromCommand(arg)[1])
                args = newArgs

        result = None

        # if func == 'map':
        #     func = args[0]
        #     args = args[1]
        #     if func in DEFINED_FUNCTIONS:
        #         result = FUNCTIONS['map'](lambda x : execute_lambda(DEFINED_FUNCTIONS[func], x), args)
        #     else:
        #         result = FUNCTIONS['map'](FUNCTIONS[func], getListFromCommand(args)[1])
        # else:
        if func in DEFINED_FUNCTIONS:
            result = execute_lambda(DEFINED_FUNCTIONS[func], args)
        else:
            result = FUNCTIONS[func](args)
    
    print(result)            ###################################################
    return str(result)

# Constructs an instance of lambda function class based on given lambda expression and returns it
def construct_lambda(args, body):
    toListFn = lambda comm : getListFromCommand(comm)[1]
    lambdaFunction = lambdas.LambdaFunction(args, body, toListFn)
    return lambdaFunction

@primitives.primitive("lambda")
def scheme_lambda(args):
    return construct_lambda(args[0], args[1])

# Takes as input an instance of lambda function class and a list of arguments
# Plugs in the arguments and executes function
def execute_lambda(lambdaFunction, args):
    return processCommand(lambdaFunction.plug(args))

# Plug in the constants defined by the user into the command/list
def plug_constants(comm):
    for constant in DEFINED_CONSTANTS:
        comm = lambdas.replaceInList(constant, DEFINED_CONSTANTS[constant], comm)
    return comm

# Given a scheme list as a single line, get it as a python list and either execute it and return result 
# or return the unchanged scheme list itself
def processCommand(comm):
    comm = plug_constants(comm)
    print(comm)                             ####################################################
    cmnd = getListFromCommand(comm)
    if cmnd[0]:     # if the command is to be executed
        # this has to be a lambda function
        if checkStartEnd(cmnd[1][0]) == 0:
            # list representing lambda function
            funcList = getListFromCommand(cmnd[1][0])[1]
            # make sure it is lambda function indeed
            assert funcList[0] == 'lambda'
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
    # remove leading ' from the list and execute the command
    return processCommand(args[0][1:])

@primitives.primitive("apply")
def scheme_apply(args):
    # list of arguments
    actArgs = getListFromCommand(args[1])
    # make sure that the list is not executable as given
    assert not actArgs[0]
    # list of arguments
    actArgs = actArgs[1]
    # function to be applied to the arguments
    func = args[0]
    # command to be processed, as python list
    actArgs.insert(0, func)
    # command to be processed, as scheme list
    comm = listToSchemeList(actArgs)
    return processCommand(comm)

@primitives.primitive("map")
def scheme_map(args):
    func = args[0]
    # given arguments for the mapped function as scheme lists
    actArgs = args[1:]
    # list of lists to use the function on
    argLists = []
    for arg in actArgs:
        argList = getListFromCommand(arg)
        # be sure that we're mapping function on a ready list
        assert not argList[0]
        argLists.append(argList[1])
    
    res = []

    for i in range(len(argLists[0])):
        # command to execute to get a single element in the to-be-returned list
        cmnd = []
        cmnd.append(func)
        for j in range(len(argLists)):
            cmnd.append(argLists[j][i])
        # turn the command into a scheme-style command as a string
        comm = listToSchemeList(cmnd)
        # compute element of the result list and append it to the result list
        res.append(processCommand(comm))
    
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
        assert openBr >= 0
        # finish reading the command if all open brackets have been closed
        if openBr == 0:
            break
        
    return fixWhitespace(comm)

# Reads the next command from a file and returns it as one line with whitespace fixed
def getCommandFromFile(file):
    comm = ''
    openBr = 0      # keep count of open brackets
    while True:
        line = file.readline()
        comm += line
        # break the loop if no more lines to be read from file
        if not line:
            # terminate program if unclosed brackets
            assert openBr == 0
            break
        for c in line:
            # check for open and closed brackets within the command
            if c == '(':
                openBr += 1
            elif c == ')':
                openBr -= 1
        # terminate program if more closed brackets than open ones
        assert openBr >= 0
        # finish reading the command if all open brackets have been closed
        if openBr == 0:
            break
    
    if comm == '':
        return None
    
    return fixWhitespace(comm)

# Process all commands from the given file.
# Return 1 if there was a call to exit within the file, return 0 otherwise.
def processFile(filename):
    file = open(filename, 'r')
    while True:
        comm = getCommandFromFile(file)
        
        # stop reading if we reached EOF
        if comm is None:
            break

        # continue if the command was an empty line
        if comm == '':
            continue

        # print(comm)             ##############################################################

        # make sure that the input command was a list
        assert checkStartEnd(comm) <= 1

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
    assert checkStartEnd(filename) == 2
    # Return from the program if there is an exit command in the file
    if processFile(filename[1:len(filename)-1]) == 1:
        sys.exit()
    else:
        return

# Defines a constant
def define_constant(arg, val):
    DEFINED_CONSTANTS[str(arg)] = str(val)

# Defines a function for later use
def define_function(arg, val):
    # first part of the function _ the name and the arguments passed
    face = getListFromCommand(arg)[1]
    # the implementation of the function
    body = val
    name = face[0]
    # passed arguments
    args = listToSchemeList(face[1:])
    lambdaFunction = construct_lambda(args, body)
    # keep the function in the defined functions dictionary by its name
    DEFINED_FUNCTIONS[name] = lambdaFunction

# Handles define command
@primitives.primitive("define")
def scheme_define(args):
    arg = args[0]
    val = args[1]
    if checkStartEnd(arg) == 0:
        define_function(arg, val)
    else:
        define_constant(arg, val)

# Keep processing commands from stdin.
def processStdin():
    while True:
        comm = getCommandFromStdin()
        
        # print(comm)             ##############################################################
        
        # make sure that the input command was a list
        assert checkStartEnd(comm) <= 1

        # quit reading commands on (exit) command
        if comm == '(exit)':
            break

        processCommand(comm)

# Main function takes command-line arguments. 
# If the user wants to run a program from a file, then there should be one command-line argument: The name of the file.
# If there was a call to (exit) in the file, then the program terminates there.
# Otherwise, it keeps taking commands from the interpreter after being done with the file.
# If there are too many arguments or no arguments, then the commands will be taken straight from stdin.
def main(args):
    # warn the user if there were too many command line arguments
    if(len(args) > 1):
        print('Too many command line arguments, opening the application the default way.')
        print('usage: python3 interpreter.py <filename>')

    elif(len(args) == 1):
        filename = args[0]
        # don't proceed to stdin if the program exits in the given file
        if processFile(filename) == 1:
            return
    
    # process commands from stdin
    processStdin()

if __name__ == '__main__':
    main(sys.argv[1:])