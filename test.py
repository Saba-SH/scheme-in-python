import lambdas
import interpreter

def test_argv():
    print('##########################')
    print('ARGV TEST 1: 3 ARGUMENTS')
    interpreter.main(['foo', 'bar', 'baz'])
    print('\nARGV TEST 2: 2 ARGUMENTS')
    interpreter.main(['foo', 'bar'])
    print('\nARGV TEST 3: 1 ARGUMENT')
    interpreter.main(['foo'])
    print('\nARGV TEST 4: 0 ARGUMENTS')
    interpreter.main([])
    print('###########################')

def test_whitespace():
    assert interpreter.fixWhitespace('aaabbbccc') == 'aaabbbccc'
    print('TEST 1 PASSED')
    assert interpreter.fixWhitespace('aaa bbb ccc') == 'aaa bbb ccc'
    print('TEST 2 PASSED')
    assert interpreter.fixWhitespace(' aaa   bbb  ccc') == 'aaa bbb ccc'
    print('TEST 3 PASSED')
    assert interpreter.fixWhitespace("aaa    bbb            eee \n ppp           \n") == 'aaa bbb eee ppp'
    print('TEST 4 PASSED')
    assert interpreter.fixWhitespace('\t\n aaa bbb \t\n ccc') == 'aaa bbb ccc'
    print('TEST 5 PASSED')
    print('\nWHITESPACE PASSED\n')

def test_input():
    print(interpreter.processFile('coms.txt'))
    # interpreter.processStdin()

def test_startEnd():
    assert interpreter.checkStartEnd('(AAAAA)') == 0
    print('TEST 2 PASSED')
    assert interpreter.checkStartEnd('\'(AAAAA)') == 1
    print('TEST 1 PASSED')
    assert interpreter.checkStartEnd('\'AAAAA\'') == 2
    print('TEST 3 PASSED')
    assert interpreter.checkStartEnd('\"AAAAA\"') == 2
    print('TEST 4 PASSED')
    assert interpreter.checkStartEnd('AAAAA') == 3
    print('TEST 5 PASSED')
    assert interpreter.checkStartEnd('(AAAAA\'') == 3
    print('TEST 6 PASSED')
    assert interpreter.checkStartEnd('\'AAAAA\"') == 3
    print('TEST 7 PASSED')

def test_encased():
    assert interpreter.getEncasedIn('AAAAA BBBBB', 0, '(', ')') == ''
    print('TEST 1 PASSED')
    assert interpreter.getEncasedIn('\'(AAAAA (exit) BBBBB)', 2, '(', ')') == '(exit)'
    print('TEST 2 PASSED')
    assert interpreter.getEncasedIn('((AAAAA BBBBB))', 1, '(', ')') == '(AAAAA BBBBB)'
    print('TEST 3 PASSED')
    assert interpreter.getEncasedIn('\'(AAAAA BBBBB (BBBBB BBBBB))', 12, '(', ')') == '(BBBBB BBBBB)'
    print('TEST 4 PASSED')
    assert interpreter.getEncasedIn('\'(AAAAA BBBBB (BBBBB BBBBB))', 6, '(', ')') == '(BBBBB BBBBB)'
    print('TEST 5 PASSED')
    assert interpreter.getEncasedIn('\'(AAAAA BBBBB ((BBBBB BBBBB)', 12, '(', ')') == ''
    print('TEST 6 PASSED')
    assert interpreter.getEncasedIn('\'(AAAAA BBBBB ((BBBBB BBBBB)))', 12, '((', '))') == '((BBBBB BBBBB))'
    print('TEST 7 PASSED')
    assert interpreter.getEncasedIn('[[[[ [[[[AAAAA BBBBB))) )))', 2, '[[[[', ')))') == '[[[[AAAAA BBBBB)))'
    print('TEST 8 PASSED')

def test_getList():
    assert interpreter.getListFromCommand('(AAAAA BBBBB)') == [True, ['AAAAA', 'BBBBB']]
    print('TEST 1 PASSED')
    assert interpreter.getListFromCommand('\'(AAAAA (exit) BBBBB)') == [False, ['AAAAA', '(exit)', 'BBBBB']]
    print('TEST 2 PASSED')
    assert interpreter.getListFromCommand('((AAAAA BBBBB))') == [True, ['(AAAAA BBBBB)']]
    print('TEST 3 PASSED')
    assert interpreter.getListFromCommand('\'(AAAAA BBBBB (BBBBB BBBBB))') == [False, ['AAAAA', 'BBBBB', '(BBBBB BBBBB)']]
    print('TEST 4 PASSED')
    assert interpreter.getListFromCommand('((AAAAA) BBBBB)') == [True, ['(AAAAA)', 'BBBBB']]
    print('TEST 5 PASSED')
    assert interpreter.getListFromCommand('(\'(BBBBB AAAAA) \'(BBBBB) AAAAA BBBBB (BBBBB BBBBB) AAAAA)') == [True, ['\'(BBBBB AAAAA)', '\'(BBBBB)', 'AAAAA', 'BBBBB', '(BBBBB BBBBB)', 'AAAAA']]
    print('TEST 6 PASSED')
    assert interpreter.getListFromCommand('\'()') == [False, []]
    print('TEST 7 PASSED')

def test_toList():
    assert interpreter.listToSchemeList([1, 2, 3, 4, 5]) == '(1 2 3 4 5)'
    print('TEST 1 PASSED')
    assert interpreter.listToSchemeList([]) == '()'
    print('TEST 2 PASSED')
    assert interpreter.listToSchemeList([[1, 2, 3], [4, 5, 6]]) == '((1 2 3) (4 5 6))'
    print('TEST 3 PASSED')
    assert interpreter.listToSchemeList(['-', ['+', '1', '-5'], '20', ['*', '8', '-1']]) == '(- (+ 1 -5) 20 (* 8 -1))'
    print('TEST 4 PASSED')

def test_replace():
    assert lambdas.replaceInList('x', '5', '(x y (x 5 o 4) xyx x)') == '(5 y (5 5 o 4) xyx 5)'
    print('TEST 1 PASSED')
    assert lambdas.replaceInList('AUA', '70', '(AUA UAUA AUAU AUA UAU (AUA UAUAUA AUA)') == '(70 UAUA AUAU 70 UAU (70 UAUAUA 70)'
    print('TEST 2 PASSED')
    assert lambdas.LambdaFunction('(x y)', '(+ x y)', lambda comm : interpreter.getListFromCommand(comm)[1]).plug('(1 2)') == '(+ 1 2)'
    print('TEST 3 PASSED')
    assert lambdas.LambdaFunction('(AUA UAU)', '(+ (* AUA UAU) UAUA AUA UAUAU (/ UAU AUA))', lambda comm : interpreter.getListFromCommand(comm)[1]).plug('(500 5)') == '(+ (* 500 5) UAUA 500 UAUAU (/ 5 500))'
    print('TEST 4 PASSED')

def test_lambda():
    lambdaFunction = None
    lambdaFunction = interpreter.construct_lambda('(x y)', '(+ x y)')
    assert interpreter.execute_lambda(lambdaFunction, [1, 2]) == interpreter.execute_lambda(lambdaFunction, '(1 2)') == '3'
    print('TEST 1 PASSED')
    lambdaFunction = interpreter.construct_lambda('(a b c)', '(* 8 (/ a b) (- 2 c))')
    assert interpreter.execute_lambda(lambdaFunction, [3, 2, 4]) == interpreter.execute_lambda(lambdaFunction, '(3 2 4)') == '-24.0'
    print('TEST 2 PASSED')

def main():
    test_lambda()

if __name__ == '__main__':
    main()