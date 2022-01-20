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

class LambdaFunction:
    def plug(self, argVals):
        execable = self.body
        argNames = self.toListFn(self.args)
        if not isinstance(argVals, list):
            argVals = self.toListFn(argVals)

        for i in range(len(argNames)):
            execable = replaceInList(argNames[i], argVals[i], execable)
            
        return execable

    def __str__(self):
        return '{Lambda Function: Arguments: \'' + self.args + '\'; ' + 'Body: \'' + self.body + '\'.}'

    # construct an instance of lambda function class based on input
    # body and args are scheme type lists in string form that can be parsed by toListFn
    def __init__(self, args, body, toListFn):
        self.args = args
        self.body = body
        self.toListFn = toListFn