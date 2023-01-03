
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
while True:
    expression = input('>> ')
    low = expression.lower()
    if low == 'exit' or low == 'quit' or low == 'q':
        exit()
    
    # surround operators with white space
    exp = []
    term = ''
    cont_flag = False
    for i in range(len(expression)):
        dig = expression[i]
        if dig.isspace():
            continue
        if not dig.isnumeric() and dig not in OPERATORS and dig not in PARENTHESES:
            print('Syntax Error: Expression must contain numerical values and valid operators only.')
            cont_flag = True
            break
        
        if dig in OPERATORS:
            exp.append(term)
            exp.append(dig)
            term = ''
        else:
            term += dig
            if i == (len(expression) - 1):
                exp.append(term)
    if cont_flag:
        continue
    
    answer = block(exp)
    if answer == None:
        continue
    print('%s\n' % answer[0])
