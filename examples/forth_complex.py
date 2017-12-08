from io import StringIO
import re
import inspect
from typing import Iterator, io, Union, Tuple, Any, List, Callable, Dict, Optional


class ParserError(Exception):
    pass


class Identifier(str): pass
class EOL: pass

TokenType = Union[Identifier, str, int, float, EOL]

# '\\{key}' from this map is replaced by according '{value}'
ESCAPED = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}


def tokenize(input_fd: io.TextIO) -> Iterator[Tuple[Optional[str], int, int]]:
    """
    Read characters from input file one-by-one and generate stream of tokens with metadata, separated by spaces or ';'
    ';' and \n are replaced by None, meaning end of line
    escaped characters in string literal are unescaped.
    Generate tuples (value:str_or_none, line:int, start_position_in_line:int)
    """
    curr_buff = None   # current token or None is no active token
    line_num = 0
    line_pos = 0
    in_str = False  # true, if now parsing string literal (==in quotes)
    token_start_line = None   # line_num & line_pos at the beginning of current token
    token_start_pos = None
    eof_reached = False

    while not eof_reached:
        ch = input_fd.read(1)

        if ch == '':
            ch = '\n'   # hack to flush current buffer
            eof_reached = True

        line_pos += 1

        if in_str:
            if ch == '\\':
                ch = input_fd.read(1)
                if ch == '':
                    return

                line_pos += 1

                if ch not in ESCAPED:
                    raise  ParserError("Failed to parse at line ...")

                curr_buff += ESCAPED[ch]
            elif ch == '"':
                yield curr_buff + '"', token_start_line, token_start_pos
                token_start_pos = None
                token_start_line = None
                curr_buff = None
                in_str = False
            elif ch == '\n':
                raise ParserError("Failed to parse at line ...")
            else:
                curr_buff += ch
        elif ch == '"':
            in_str = True
            curr_buff = ch
            token_start_pos = line_pos
            token_start_line = line_num
        elif ch.isspace():
            if curr_buff is not None:
                yield curr_buff, token_start_line, token_start_pos
                curr_buff = None
                token_start_pos = None
                token_start_line = None

            if ch == '\n':
                yield None, line_num, line_pos
                line_num += 1
                line_pos = 0

        elif ch == ';':
            yield None, line_num, line_pos
        else:
            if curr_buff is None:
                curr_buff = ch
                token_start_pos = line_pos
                token_start_line = line_num
            else:
                curr_buff += ch


def typed_tokenize(tokens: Iterator[Tuple[Optional[str], int, int]]) -> Iterator[Tuple[TokenType, int, int]]:
    """
    Transform stream of untyped tokens into stream of typed tokens
    Merge subsequent EOL into single EOL
    """
    prev_eol = False  # mean th
    for value, line, pos in tokens:
        if value is None:
            if not prev_eol:
                yield EOL(), line, pos
        elif value[0] == '"':
            assert value[-1] == '"', "Incorrect string literal {!r} at {}:{}".format(value, line, pos)
            yield value[1:-1], line, pos
        else:
            for tp in (int, float):
                try:
                    yield tp(value), line, pos
                    break
                except (ValueError, TypeError):  # get there is token not int/float
                    pass
            else:
                assert re.match('[_a-zA-Z][_0-9a-zA-Z]*$', value), \
                    "Incorrect identifier {!r} at {}:{}".format(value, line, pos)
                yield Identifier(value), line, pos

        prev_eol = value is None


# global dictionary, which map command name to command function
CMDS = {}

def cmd(stack_used: int = None, nparams: int = 0, name: str = None, vars: bool = False) \
        -> Callable[[Callable], Callable]:
    """decorator to mark commands
    stack_used - number of parameters from stack are used or None to detect stack parameters count from
        func description
    nparams - number of parameters, which must came from forth source code for this command
    name - name of command, is not set func.__name__ is used
    vars - True is function need access to variables
    """
    def closure(func: Callable) -> Callable:
        if stack_used is None:
            # inspect.signature(func).parameters return tuple of function 'func' parameter names
            # -1/-2 is for stack[and vars] arguments, which must always be the first two parameters
            func.nstack = len(inspect.signature(func).parameters) - nparams - (2 if vars else 1)
        else:
            func.nstack = stack_used

        func.vars = vars
        func.nparams = nparams
        CMDS[func.__name__ if name is None else name] = func

        return func
    return closure


def run(ttokens: Iterator[Tuple[TokenType, int, int]], stack: List[Any] = None,
        vars: Dict[str, Any] = None) -> None:
    """Execution loop
    Get generator of tokens, initial stack value and initial variables values
    Run program with given stack"""

    stack = [] if stack is None else stack
    vars = {} if vars is None else vars

    for token, line, pos in ttokens:
        if isinstance(token, EOL):
            continue

        assert isinstance(token, Identifier)

        func = CMDS[token]

        params = [next(ttokens)[0] for i in range(func.nparams)]
        sparams = [stack.pop() for i in range(func.nstack)]

        if func.vars:
            func(stack, vars, *(params + sparams))
        else:
            func(stack, *(params + sparams))



# Commands
@cmd(nparams=1, vars=True)
def put(stack, vars, value):
    """put VALUE - put value on top of stack"""
    if isinstance(value, Identifier):
        value = vars[str(value)]
    stack.append(value)

@cmd(nparams=2, vars=True)
def set(_, vars, name, val):
    """set NAME VALUE - set value 'val' to variable 'name'"""
    assert isinstance(name, Identifier)
    vars[str(name)] = val

@cmd()
def pop(stack):
    stack.pop()

@cmd()
def show(stack):
    print(stack.pop())

@cmd()
def shown(stack):
    print(stack.pop(), end='')

@cmd()
def add(stack, v1, v2):
    stack.append(v1 + v2)

@cmd()
def sub(stack, v1, v2):
    stack.append(v1 - v2)

@cmd()
def dup(stack, v1):
    stack.append(v1)
    stack.append(v1)

@cmd()
def div(stack, v1, v2):
    stack.append(v1 / v2)

@cmd()
def mul(stack, v1, v2):
    stack.append(v1 * v2)

@cmd()
def sqrt(stack, v1):
    stack.append(v1 ** 0.5)
    stack.append(-(v1 ** 0.5))

@cmd()
def swap(stack, v1, v2):
    stack.append(v2)
    stack.append(v1)

@cmd()
def neg(stack, v1):
    stack.append(-v1)


if __name__ == "__main__":
    # solving square equation in form ax**2 + bx + c = 0
    program = """
    set a 1.0
    set b 0
    set c -1.0

    put a
    put c
    put 4
    mul
    mul
    put b
    put b
    mul
    sub
    sqrt
    
    put b
    neg
    add
    put 2
    put a
    mul
    div
    
    put "result1 = "
    shown
    show
    
    put b
    neg
    add
    put 2
    put a
    mul
    div
    
    put "result2 = "
    shown
    show
    """

    # data = StringIO(program)
    # for is_str, tok, *_ in tokenize(data):
    #     print(is_str, repr(tok))

    # print("-----------------------------")
    #
    # data = StringIO(program)
    # for tok, *_ in typed_tokenize(tokenize(data)):
    #     print(tok)

    data = StringIO(program)
    tokens = typed_tokenize(tokenize(data))
    run(tokens)
