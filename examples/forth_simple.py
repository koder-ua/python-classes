import sys


def parse_code(code):
    for lineno, line in enumerate(code.split("\n"), 1):
        for command_block in line.split(";"):
            command_block = command_block.strip()

            if command_block == "" or command_block.startswith("#"):
                continue

            try:
                if " " not in command_block:
                    yield lineno, (command_block, None)
                else:
                    cmd, param = command_block.split(" ", 1)
                    if param.startswith('"') and param.endswith('"'):
                        param = param[1:-1].replace('\\\\', '\\').replace('\\n', '\n').replace('\\t', '\t')
                    else:
                        try:
                            param = int(param)
                        except ValueError:
                            param = float(param)
                    yield lineno, (cmd, param)
            except Exception:
                print("Parse error at line", lineno, file=sys.stderr)
                raise


def execute(stack, code):
    for lineno, (cmd, param) in parse_code(code):
        if cmd == "put":
            stack.append(param)
        elif cmd == "add":
            stack.append(stack.pop() + stack.pop())
        elif cmd == "sub":
            stack.append(stack.pop() - stack.pop())
        elif cmd == "print":
            print(stack.pop())
        else:
            raise ValueError("Unknown command {} at line {}".format(cmd, lineno))


execute([], "put 1; put 2; add; print")

