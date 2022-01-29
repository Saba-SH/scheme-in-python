class IfBlock:
    def getChosen(self):
        if self.execFn(self.condition) == '#f':
            return self.falseBlock
        else:
            return self.trueBlock

    def __str__(self):
        return '{If block: Condition: \'' + self.condition + '\'; True block: \'' + self.trueBlock + '\'; False block: \'' + self.falseBlock + '\'.}'

    def __init__(self, condition, trueBlock, falseBlock, execFn):
        self.condition = condition
        self.trueBlock = trueBlock
        self.falseBlock = falseBlock
        self.execFn = execFn

class CondBlock:
    def getChosen(self):
        for i in range(len(self.conditions)):
            if self.execFn(self.conditions[i]) == '#t':
                return self.blocks[i]
            
        return self.blocks[len(self.blocks) - 1]

    def __str__(self):
        repr = '{Conditional Block: '
        for i in range(len(self.conditions)):
            repr += '\n' + self.conditions[i] + '\t' + self.blocks[i]
        repr += '\nelse ' + self.blocks[len(self.blocks) - 1] + '}'

    def __init__(self, conditions, blocks, execFn):
        self.conditions = conditions
        self.blocks = blocks
        self.execFn = execFn
