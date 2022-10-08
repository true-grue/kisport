# lisp_eval("(+ 1 2)") -> 3
# ['(', '+', 1, 2, ')']
# (f a_1 a_2 ...)
 
def lisp_scan(source):
    source = source.replace('(', ' ( ')
    source = source.replace(')', ' ) ')
    return source.split()
 
def define(env, name, expr):
    env[name] = expr
 
PRIMS = {
    '+': lambda e, a, b: a + b,
    '-': lambda e, a, b: a - b,
    '*': lambda e, a, b: a * b,
    '/': lambda e, a, b: a // b,
    'define': define,
    'begin': lambda e, *a: a[-1]
}
 
def lisp_parse(tokens):
    ast = []
    while len(tokens):
        token = tokens.pop(0)
        if token == '(':
            ast.append(lisp_parse(tokens))
        elif token == ')':
            return ast
        elif token.isdigit():
            ast.append(int(token))
        else:
            ast.append(token)
    return ast[0]
 
def lisp_lambda(env, params, expr):
    def func(env, *args):
        env = env.copy()
        env.update(zip(params, args))
        return lisp_eval(env, expr)
    return func
 
MACRO = {
    "lambda": lisp_lambda
}
 
def lisp_eval(env, expr):
    if isinstance(expr, list):
        func, *args = expr
        func = lisp_eval(env, func)
        if func in MACRO:
            return MACRO[func](env, *args)
        return func(env, *[lisp_eval(env, a) for a in args])
    elif expr in env:
        return env[expr]
    else:
        return expr
 
tokens = lisp_scan('''
(begin
  (define x 10)
  (define y 20)
  (define square (lambda (x) (* x x)))
  (square 3)
)
''')

print(tokens)
expr = lisp_parse(tokens)
print(expr)
env = PRIMS.copy()
print(lisp_eval(env, expr))
