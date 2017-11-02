import math, operator as op

def tokenize(string):
    return string.replace('(', '( ').replace(')', ' ) ').split()

def parse(tokens):
    expression = []
    
    if tokens[0] == '(':
        while tokens[0] != ')':
            expression.append(type_correct(tokens.pop(0)))
            
            if tokens[0] == '(':
                expression.append(parse(tokens))

            if tokens[0] == ')':
                expression.append(tokens.pop(0))
                return expression[1:][:-1]
            

    elif tokens[0] == ')':
        raise SyntaxError("Expression begining with ')'")

    else:
        return tokens

def type_correct(string):
    if '.' in string:
        try: return float(string)
        except: SyntaxError("Inproper use of '.' in: " + string)
    
    else:
        try: return int(string)
        except: return string


def environment():
    env = {'+' : op.add,
           '-' : op.sub,
           '*' : op.mul,
           '=' : op.eq,
           '/' : op.truediv,
           'remainder' : op.mod,
           'expt' : op.pow,
           'abs' : op.abs}

    return env


def evaluate(exp, env=environment()):
    for i in range(len(exp)):
        if isinstance(exp[i], list):
            exp[i] = evaluate(exp[i], env)

    def solve():
        if len(exp) > 1:
            return operator(exp.pop(0), solve())

        else:
            return exp.pop(0)
    
    operator = env[exp.pop(0)]

    return solve()


def repl():
    while True:
        exp = input('\u03bb : ')

        if exp == '(exit)':
            return 'Goodbye, World!'

        elif exp == '':
            continue

        else:
            print(evaluate(parse(tokenize(exp))))
        

if __name__ == "__main__":
    print(repl())
