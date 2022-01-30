from utils import replaceInList

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
