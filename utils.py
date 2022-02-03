from sys import exit
"""This file implements utilities used for working with scheme I/O,
 scheme lists and using them together with python lists."""

CSE_EXECUTABLE_LIST = 0
CSE_NONEXECUTABLE_LIST = 1
CSE_STRING = 2
CSE_OTHER = 3

# Removes all the comments from the given command.
def removeComments(comm):
    pos = 0
    
    while True:
        if pos >= len(comm):
            break
        comPos = comm.find(';', pos)
        if comPos == -1:
            break
        uncomPos = comm.find('\n', comPos)
        if uncomPos == -1:
            uncomPos = len(comm)
        comm = comm[0:comPos] + comm[uncomPos + 1:]
        pos = comPos

    return comm

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
# Check for (...); '(...); '...'/"...".
def checkStartEnd(strn):
    if strn[len(strn) - 1] == ')' and strn[0] == '(':
        return CSE_EXECUTABLE_LIST
    if strn[len(strn) - 1] == ')' and strn[0:2] == '\'(':
        return CSE_NONEXECUTABLE_LIST
    if [strn[0], strn[len(strn) - 1]] in [['\'', '\''], ['\"', '\"']]:
        return CSE_STRING
    return CSE_OTHER

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
    # make sure that the command is an actual scheme list
    if checkStartEnd(comm) not in [CSE_EXECUTABLE_LIST, CSE_NONEXECUTABLE_LIST]:
        print("Error: trying to parse a non-list as a list. Quitting.")
        exit()
        
    res = []
    comm = comm[:len(comm) - 1]         # remove ) at the end
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
    return res

# Returns a string representation of the given python list(no quotes)
def listToSchemeList(lst):
    res = '('
    if len(lst) > 0:
        res += listToSchemeList(lst[0]) if isinstance(lst[0], list) else str(lst[0])
    for elem in lst[1:]:
        res += ' ' + (listToSchemeList(elem) if isinstance(elem, list) else str(elem))
    res += ')'
    return res

# Returns a string representation of the given python list, except that all lists are starting with quote
def listTononexList(lst):
    res = '\'('
    if len(lst) > 0:
        res += listTononexList(lst[0]) if isinstance(lst[0], list) else str(lst[0])
    for elem in lst[1:]:
        res += ' ' + (listTononexList(elem) if isinstance(elem, list) else str(elem))
    res += ')'
    return res


# Replaces every occurence of arg in lst with argVal. lst is a scheme list in string form.
def replaceInList(arg, argVal, lst):
    pos = 0
    while True:
        pos = lst.find(arg, pos)
        if pos == -1:
            break

        if lst[pos - 1] in ['(', ' '] and lst[pos + len(arg)] in [')', ' ']:
            lst = lst[0:pos] + str(argVal) + lst[pos + len(str(arg)):]
        
        pos += len(arg)

    return lst

# Used to output the result of a command
def output(result):
    if result is None:
        return
    if isinstance(result, list):
        result = listToSchemeList(result)
    result = str(result)
    result = result.replace('\'(', '(')
    result = fixWhitespace(result)
    print(result, end='')
