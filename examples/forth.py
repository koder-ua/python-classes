import sys

def parse_file(fd):
    for lineno, raw_line in enumerate(fd):
        line = raw_line.strip()
        if line == "" or line.startswith("#"):
            continue
        try:
            if " " not in line:
                yield lineno, (line, None)
            else:
                cmd, param = line.split(" ", 1)
                if param.startswith('"') and param.endswith('"'):
                    param = param[1:-1]
                else:
                    try:
                        param = int(param)
                    except ValueError:
                        param = float(param)
                yield lineno, (cmd, param)
        except Exception as x:
            print >>sys.stderr, "Parse error at line", lineno
            raise

def execute(stack, fd):
    for lineno, (cmd, param) in parse_file(fd):
        if cmd == "put":
            stack.append(param)
        elif cmd == "add":
            stack.append(stack.pop() + stack.pop())
        elif cmd == "sub":
            stack.append(stack.pop() - stack.pop())
        elif cmd == "print":
            print stack.pop()
        else:
            raise ValueError("Unknown command {} at line {}".format(cmd, lineno))


def execute_2():
    def put(stack, param):
        stack.append(param)

    def add(stack, _):
        stack.append(stack.pop() + stack.pop())

    def sub(stack, _):
        stack[-1] = -stack[-1]
        add(stack)

    def do_print(stack, _):
        print stack.pop()

    cmd_map = dict(put=put, sub=sub, add=add)
    cmd_map['print'] = do_print

    def execute(stack, fd):
        for lineno, (cmd, param) in parse_file(fd):
            if cmd in cmd_map:
                cmd_map[cmd](stack, param)
            else:
                raise ValueError("Unknown command {} at line {}".format(cmd, lineno))


execute([], "put 1; put 2; add; print".split(';'))


class Forth(list):
    def execute(self, fd):
        execute(self, fd)
