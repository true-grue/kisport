# Разработка интерпретатора 1С на языке Python.
#
# 1. Транслятор - средство перевода текста
# программы с одного языка программирования
# на другой. Примеры трансляторов:
# - TypeScript > JavaScript (TSC),
# - C > Assembly Language (gcc),
# - C > Web Assembler (Emscripten),
# - C > JavaScript (Emscripten).
# КОД -> КОД
#
# 2. Интепретатор - транслятор в результат.
# Примеры:
# - Интерпретатор Lua,
# - Интерпретатор Python.
# КОД -> РЕЗУЛЬТАТ
#
# 3. Компилятор - транслятор текста программы
# на языке высокого уровня в машинный код
# (Assembly Language, Common Intermediate
#  Language и др.).
# КОД -> МАШИННЫЙ КОД

# Процесс интерпретации:
# СТРОКА -> ТОКЕНЫ -> ДЕРЕВО СИНТАКСИСА -> РЕЗУЛЬТАТ
#
# 1. Лексический анализ (токенизация).
#    СТРОКА -> ТОКЕНЫ
# Пример: "A = 10;" -> [ID, EQ, NUM, SCOL]
#
# 2. Синтаксический анализ (разбор).
#    ТОКЕНЫ -> ДЕРЕВО СИНТАКСИСА
# Пример: [ID, EQ, NUM, SCOL] -> ('assign', 'a', 10)
#
# 3. Интерпретация дерева синтаксиса.
#    ДЕРЕВО СИНТАКСИСА -> РЕЗУЛЬТАТ
# Пример: ('assign', 'a', 10) -> {"a": 10}
#
# Библиотека sly для языка Python:
# https://github.com/dabeaz/sly
# Документация к библиотеке sly:
# https://sly.readthedocs.io/en/latest/

from sly.src.sly import Lexer, Parser
from pprint import pprint


class Mini1CLexer(Lexer):
    tokens = {ID, EQ, NUM, SCOL, STR,
              PROC, ENDPROC, LB, RB,
              COMMA}
    ID = r'[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я_0-9]*'
    ID[r'Процедура'] = PROC
    ID[r'КонецПроцедуры'] = ENDPROC
    LB = r'\('
    RB = r'\)'
    EQ = r'='
    SCOL = r';'
    COMMA = r','
    ignore_spaces = r' |\t|\n'
    ignore_comment = r'//.*'

    @_(r'[0-9]+')
    def NUM(self, token):
        token.value = int(token.value)
        return token

    @_(r'("[^"]*")|(\'[^\']*\')')
    def STR(self, token):
        token.value = token.value[1:-1]
        return token


# Форма Бэкуса-Наура (БНФ)
# Правильная скобочная последовательность:
# <правпосл> ::= <пусто>
#              | (<правпосл>)
#              | <правпосл><правпосл>
# Пример: '', '()', '(())', '()()'


class Mini1CParser(Parser):
    tokens = Mini1CLexer.tokens

    @_('{ procedure } { statement }')
    def block(self, p):
        return ('block', p.procedure, p.statement)

    # Процедура МояПроцедура ( параметры ) блок КонецПроцедуры
    @_('PROC ID LB parameters RB block ENDPROC')
    def procedure(self, p):
        return ('proc', p.ID, p.parameters, p.block)

    # Параметр1 ,Параметр2 ,Параметр3
    @_('ID { COMMA ID }')
    def parameters(self, p):
        return [p.ID0] + p.ID1

    # Параметры отсутствуют.
    @_('')
    def parameters(self, p):
        return []

    # Сообщить ( аргументы ) ;
    @_('ID LB arguments RB SCOL')
    def statement(self, p):
        return ('call', p.ID, p.arguments)

    # ( "Значение" ,42 ,43 )
    @_('value { COMMA value }')
    def arguments(self, p):
        return [p.value0] + p.value1

    # Аргументы отсутствуют.
    @_('')
    def arguments(self, p):
        return []

    # A = value ;
    @_('ID EQ value SCOL')
    def statement(self, p):
        return ('assign', p.ID, p.value)

    # МояПроцедура
    @_('ID')
    def value(self, p):
        return ('var', p.ID)

    # 42
    @_('NUM')
    def value(self, p):
        return ('number', p.NUM)

    # "Hello"
    @_('STR')
    def value(self, p):
        return ('str', p.STR)


def interpret(env, ast):
    spec, *args = ast
    if spec == "block":
        procs = args[0]
        statements = args[1]
        for proc in procs + statements:
            interpret(env, proc)
    elif spec == "proc":
        name, params, stmts = args
        env[name] = (params, stmts)
    elif spec == "assign":
        name, value = args
        env[name] = interpret(env, value)
    elif spec == "call":
        name, values = args
        function = env[name]
        if isinstance(function, tuple):
            params, stmts = function
            local = env.copy()
            for i in range(len(params)):
                name = params[i]
                value = values[i]
                local[name] = interpret(env, value)
            interpret(local, stmts)
        else:
            params = [interpret(env, a) for a in values]
            function(*params)
    elif spec == "var":
        return env[args[0]]
    elif spec in ("number", "str"):
        return args[0]


code = '''
Процедура МояПроцедура(ВтороеСообщение)
    Сообщение = "Документ изменен.";
    Сообщить(Сообщение);
    Сообщить(ВтороеСообщение);
КонецПроцедуры

A = 42; // Это – комментарий
ПримерПеременной = "Привет, 1С!";
ПустаяСтрока = "";

Сообщить(ПримерПеременной);
Сообщить(A);
МояПроцедура("Данные удалены.");
'''

lexer = Mini1CLexer()
parser = Mini1CParser()

# Лексический анализ (токенизация).
tokens = list(lexer.tokenize(code))
print("\nТокены:")
pprint(tokens)

# Синтаксический анализ
# (построение дерева синтаксиса).
tree = parser.parse(iter(tokens))
print("\nДерево:")
pprint(tree)


def message(text):
    print(text)


# Интерпретация дерева синтаксиса.
print("\nВывод:")
env = {"Сообщить": message}
interpret(env, tree)
