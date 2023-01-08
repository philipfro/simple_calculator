
print('\nThe following operators are valid: \'+, -, *, /, ^\', as well as parentheses.')
print('Type \'ans\' to use the previous answer in an expression.')
print('Enter \'exit\', \'quit\', or \'q\' to exit the program.\n')


OPERATORS = ['+', '-', '*', '/', '^']
PARENTHESES = ['(', ')']

# recurse inside each parentheses block
def block(words: list):
    parts = words
    
    # parentheses
    for i in range(len(parts)):
        if (i < len(parts)) and parts[i][0] == '(':
            if i == (len(parts) - 1):
                print('Syntax Error: parentheses cannot be opened at end of expression.')
                return None
            
            parts[i] = parts[i][1:]
            # get what's inside the parentheses
            inside = []
            blocks = 0
            while (i < len(parts)) and ((parts[i][len(parts[i]) - 1] != ')') or (blocks > 0)):
                if parts[i][0] == '(':
                    blocks += 1
                elif parts[i][len(parts[i]) - 1] == ')':
                    blocks -= 1
                inside.append(parts[i])
                parts = parts[:i] + parts[(i + 1):]
            if i >= len(parts):
                print('Syntax Error: parentheses must be closed.')
                return None
            inside.append(parts[i][:(len(parts[i]) - 1)])
            
            parts[i] = block(inside)[0] # operate on inside expression
    
    # exponents
    for i in range(len(parts)):
        if (i < len(parts)) and parts[i] == '^':
            if not check_ops(parts, i, '^'):
                return None
            
            parts[i - 1] = float(parts[i - 1]) ** float(parts[i + 1])
            parts = parts[:i] + parts[(i + 2):]
    
    # multiplication
    for i in range(len(parts)):
        if (i < len(parts)) and parts[i] == '*':
            if not check_ops(parts, i, '*'):
                return None
            
            parts[i - 1] = float(parts[i - 1]) * float(parts[i + 1])
            parts = parts[:i] + parts[(i + 2):]
    
    # division
    for i in range(len(parts)):
        if (i < len(parts)) and parts[i] == '/':
            if not check_ops(parts, i, '/'):
                return None
            
            parts[i - 1] = float(parts[i - 1]) / float(parts[i + 1])
            parts = parts[:i] + parts[(i + 2):]
    
    # addition
    for i in range(len(parts)):
        if (i < len(parts)) and parts[i] == '+':
            if not check_ops(parts, i, '+'):
                return None
            
            parts[i - 1] = float(parts[i - 1]) + float(parts[i + 1])
            parts = parts[:i] + parts[(i + 2):]
    
    # subtraction
    for i in range(len(parts)):
        if (i < len(parts)) and (parts[i] == '-'):
            if not check_ops(parts, i, '-'):
                return None
            
            parts[i - 1] = float(parts[i - 1]) - float(parts[i + 1])
            parts = parts[:i] + parts[(i + 2):]
    
    return parts


def check_ops(parts: list, i, op: str) -> bool:
    if (i == 0) or (i == (len(parts) - 1)):
        print('Syntax Error: \"%s\" cannot be at edge of expression.' % (op))
        return False
    if ((parts[i - 1] in OPERATORS) or (parts[i + 1] in OPERATORS)):
        print('Syntax Error: \"%s\" must be surrounded by numerical values.' % (op))
        return False
    return True


# accepts inputs repeatedly until user quits
prev = None
while True:
    expression = input('>> ')
    low = expression.lower()
    if low == 'exit' or low == 'quit' or low == 'q':
        exit()
    
    # surround operators with white space
    exp = []
    term = ''
    cont_flag = False
    i = 0
    while i < len(expression):
        dig = expression[i]
        if dig.isspace():
            i += 1
            continue
        
        ans = expression[i:(i + 3)] == 'ans'
        if not dig.isnumeric() and dig not in OPERATORS and dig not in PARENTHESES and not ans:
            print('Syntax Error: Expression must contain numerical values and valid operators only.')
            cont_flag = True
            break
        if ans:
            if prev == None:
                print('Error: There is no valid previous answer to use.')
                cont_flag = True
                break
            dig = prev
        if dig in OPERATORS:
            exp.append(term)
            exp.append(dig)
            term = ''
        else:
            term += dig
            if i == (len(expression) - 1) or (ans and (i == len(expression) - 3)):
                exp.append(term)
        i += 3 if ans else 1
    if cont_flag:
        continue
    
    answer = block(exp)
    if answer == None:
        prev = None
        continue
    prev = str(answer[0])
    print('%s\n' % answer[0])
