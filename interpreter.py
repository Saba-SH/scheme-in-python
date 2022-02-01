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
    if (isinstance(func, lambdas.LambdaFunction)) or (func not in ['if', 'cond', 'define', 'lambda']):
        for i in range(len(args)):
            if utils.checkStartEnd(args[i]) == utils.CSE_EXECUTABLE_LIST:
                args[i] = processCommand(args[i])
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

        # if func == 'map':
        #     func = args[0]
        #     args = args[1]
        #     if func in DEFINED_FUNCTIONS:
        #         result = FUNCTIONS['map'](lambda x : execute_lambda(DEFINED_FUNCTIONS[func], x), args)
        #     else:
        #         result = FUNCTIONS['map'](FUNCTIONS[func], utils.getListFromCommand(args)[1])
        # else:
        if func in DEFINED_FUNCTIONS:
            result = execute_lambda(DEFINED_FUNCTIONS[func], args)
        else:
            result = FUNCTIONS[func](args)
    
    if func in ["cdr", "cons", "append"]:
        result = utils.listTononexList(result)

    if result is not None and isinstance(result, str) and utils.checkStartEnd(result) in [utils.CSE_EXECUTABLE_LIST, utils.CSE_NONEXECUTABLE_LIST]:
        result = utils.fixWhitespace(result)

    # print(result)            ###################################################
    # if not isinstance(result, lambdas.LambdaFunction):
    #     result = str(result)
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
    # print(comm)                             ####################################################
    cmnd = utils.getListFromCommand(comm)
    if cmnd[0]:     # if the command is to be executed
        # this has to be a lambda function
        if utils.checkStartEnd(cmnd[1][0]) == utils.CSE_EXECUTABLE_LIST:
            # list representing lambda function
            funcList = utils.getListFromCommand(cmnd[1][0])[1]
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
    if isinstance(args[1], str) and utils.checkStartEnd(args[1]) == utils.CSE_NONEXECUTABLE_LIST:
        actArgs = utils.getListFromCommand(args[1])[1]
    else:
        actArgs = args[1]
    # # make sure that the list is not executable as given  ###################
    # assert not actArgs[0] #####################
    # list of arguments     #####################
    # actArgs = actArgs[1]  #####################
    # function to be applied to the arguments
    func = args[0]
    # # command to be processed, as python list     ################
    # actArgs.insert(0, func)               ##############
    # # command to be processed, as scheme list     #############
    # comm = utils.listToSchemeList(actArgs)    ############
    # return processCommand(comm)           ##############
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
        assert not argList[0]
        argLists.append(argList[1])
    
    res = []

    for i in range(len(argLists[0])):
        # command to execute to get a single element in the to-be-returned list
        cmnd = []
        cmnd.append(func)
        for j in range(len(argLists)):
            cmnd.append(argLists[j][i])
        # # turn the command into a scheme-style command as a string
        # comm = utils.listToSchemeList(cmnd)
        # # compute element of the result list and append it to the result list
        # res.append(processCommand(comm))
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
        assert openBr >= 0
        # finish reading the command if all open brackets have been closed
        if openBr == 0:
            break
        
    return utils.fixWhitespace(utils.removeComments(comm))

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
    
    return utils.fixWhitespace(utils.removeComments(comm))

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
        assert utils.checkStartEnd(comm) in [utils.CSE_EXECUTABLE_LIST, utils.CSE_NONEXECUTABLE_LIST]

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
        print("Invalid input. Make sure to use brackets.")
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
        
        # print(comm)             ##############################################################
        
        # make sure that the input command was a list
        assert utils.checkStartEnd(comm) in [utils.CSE_EXECUTABLE_LIST, utils.CSE_NONEXECUTABLE_LIST]

        # quit reading commands on (exit) command
        if comm == '(exit)':
            break

        result = processCommand(comm)
        
        utils.output(result)    #    UNCOMMENT   UNCOMMENT   UNCOMMENT   UNCOMMENT   UNCOMMENT
        if result is not None:
            print('')

# Main function takes command-line arguments. 
# If the user wants to run a program from a file, then there should be a command-line argument: The name of the file.
# If there are too many arguments or no arguments, then the commands will be taken straight from stdin.
def main(args):
    # warn the user if there were too many command line arguments
    if(len(args) > 1):
        print('Too many command line arguments, opening the application the default way.')
        print('usage: python3 interpreter.py <filename>')

    elif(len(args) == 1):
        filename = args[0]
        processFile(filename)
        return
    
    # process commands from stdin
    processStdin()

if __name__ == '__main__':
    main(sys.argv[1:])
