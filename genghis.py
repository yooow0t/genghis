import math, operator as op

def tokenize(string):
    return string.replace('(', '( ').replace(')', ' ) ').split()

def parse(tokens):
    expression = []

    if tokens[0] == '(':
        tokens.pop(0)

    while tokens:
        if tokens[0] == '(': 
            expression.append(parse(tokens))

        elif tokens[0] == ')':
            tokens.pop(0)
            return expression

        else:
            expression.append(type_correct(tokens.pop(0)))

    return expression   
        

def type_correct(string):
    if '.' in string:
        try: return float(string)
        except: SyntaxError("Inproper use of '.' in: " + string)
    
    else:
        try: return int(string)
        except: return string


def initial_env():
    env = {'+' : op.add,
           '-' : op.sub,
           '*' : op.mul,
           '=' : op.eq,
           '/' : op.truediv,
           '>' : op.gt,
           '<' : op.lt,
           '>=' : op.ge,
           '=>' : op.le,
           '!=' : op.ne,
           'not' : op.__not__,
           'and' : op.__and__,
           'or' : op.__or__,
           '#t' : True,
           '#f' : False,
           'remainder' : op.mod,
           'expt' : op.pow,
           'abs' : op.abs,
           'if' : 'if',
           'define': 'define'}

    return env


def evaluate(exp, env):
    if exp[0] != 'define':
        for i in range(len(exp)):
            if isinstance(exp[i], list):
                operator = exp[i][0]
                arg1 = exp[i][1]
                if operator != 'define' and not isinstance(arg1, list):
                    exp[i] = evaluate(exp[i], env)[0]

    exp_len = len(exp)
                                
    def solve():
        if operator == 'if':
            if exp[0]:
                exp[2]
                return exp[1]
            else:
                exp[1]
                return exp[2]
        
        elif operator == 'define':
            var = exp[0]
            if isinstance(var, list):
                name = var[0]
                args = list(var[1:])
                body = list(exp[1])
                env[name] = lambda *x : function_eval(body, args, env, x)
                return env[name]

            elif isinstance(var, str):
                env[var] = exp[1]
                return exp[1]
            else:
                raise TypeError("numbers may not be redefined")

        elif len(exp) > 1:
            return operator(exp.pop(0), solve())

        else:
            return exp.pop(0)

    operator = env[exp.pop(0)]

    if "lambda" in str(operator):
        return operator(*exp), env

    if operator != 'define':
        for i in range(len(exp)): 
            if isinstance(exp[i], str):
                exp[i] = env[exp[i]]

    return solve(), env


def function_eval(body, args, env, x):
    for i in range(len(args)):
        for n in range(len(body)):
            if body[n] == args[i]:
                body[n] = x[i]

    return evaluate(body, env)[0] 


def repl():
    user_env = {}
    user_env.update(initial_env())
    user_env["square"] = lambda *x : function_eval(["*", "x", "x"], ["x"], user_env, x)

    while True:
        exp = input('\u03bb : ')

        if exp == '(exit)':
            return 'Goodbye, World!'

        elif exp == '':
            continue

        else:
            out, user_env = evaluate(parse(tokenize(exp)), user_env)
            print(out)

if __name__ == "__main__":
    print(repl())
