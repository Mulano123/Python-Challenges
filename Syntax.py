class ILexType:
    pass

class LexContainer(ILexType):
    def __init__(self):
        self.items = []

class LexValue(ILexType):
    def __init__(self, value, is_expression):
        self.value = value
        self.is_expression = is_expression

def parse_exp(exp):
    if not exp.strip():
        return

    print(f"Sentence: {exp}")
    print("- <assign> => ")

    c = parse(list(filter(lambda c: not c.isspace() and (c.isalnum() or is_operator(c)), exp)))

    print(f"\t| {format_exp('<assign>', c, 0)}\n")

def format_exp(expression, c, sub):
    if not c.items or not expression.strip():
        return ""
    if "<assign>" in expression:
        expression = "<id> = <expr>"

    while c.items:
        sb = f"\t| {expression}"
        if sub > 0:
            for i in range(sub):
                sb += ')'
                if i + 1 < sub:
                    sb += " <cont>"

        print(sb)

        t = c.items[0]

        if "<id>" in expression:
            if not isinstance(t, LexValue) or not t.is_expression:
                raise ValueError("Invalid expression found.")
            expression = expression.replace("<id>", str(t.value))

            c.items.pop(0)
            if not c.items:
                break
            t = c.items[0]

            if (not isinstance(t, LexValue) or t.is_expression
                    or t.value not in expression):
                raise ValueError("Invalid value found.")

            c.items.pop(0)
            continue

        if "<expr>" in expression:
            if isinstance(t, LexValue):
                if not t.is_expression:
                    raise ValueError(f"'{t.value}' expected.")
                if not c.items:
                    raise ValueError("Syntax error.")

                if len(c.items) > 1:
                    iop = c.items[1]
                    if isinstance(iop, LexValue):
                        if iop.is_expression:
                            raise ValueError(f"'{iop.value}' expected.")
                        expression = expression.replace("<expr>", f"<id> {iop.value} <expr>")
                    continue

                expression = expression.replace("<expr>", "<id>")
                continue

            if isinstance(t, LexContainer):
                c.items.pop(0)

                op_idx = next((i for i, itm in enumerate(t.items) if isinstance(itm, LexValue) and not itm.is_expression), -1)
                if op_idx == -1:
                    raise ValueError("Syntax error.")
                lv = t.items[op_idx]
                expression = expression.replace("<expr>", f"(<id> {lv.value} <expr>")
                expression = format_exp(expression, t, sub + 1)

                if c.items:
                    t = c.items[0]
                    if not isinstance(t, LexValue) or t.is_expression:
                        raise ValueError("Syntax error.")
                    sb = expression
                    sb += f" {t.value} <expr>"
                    expression = sb
                    c.items.pop(0)
                    continue

    if sub > 0:
        expression += ")"
    return expression

def parse(exp):
    lex_container = LexContainer()
    while exp:
        if exp[0].isalnum():
            lex_container.items.append(LexValue(exp[0], True))
            exp = exp[1:]
            continue
        if is_operator(exp[0]):
            if exp[0] == '(':
                close_parenthesis_idx = get_close_parenthesis_index(exp)
                if close_parenthesis_idx == -1:
                    raise ValueError("Imbalance parentheses.")
                new_array = exp[1:close_parenthesis_idx]
                lex_container.items.append(parse(new_array))
                exp = exp[close_parenthesis_idx + 1:]
                continue
            lex_container.items.append(LexValue(exp[0], False))
            exp = exp[1:]
    return lex_container

def get_close_parenthesis_index(c):
    if not c:
        return -1
    open_parentheses = []
    for i in range(len(c)):
        if c[i] == '(':
            open_parentheses.append('(')
            continue
        if c[i] == ')':
            if not open_parentheses:
                return -1
            open_parentheses.pop()
            if not open_parentheses:
                return i
    return -1

def is_operator(c):
    return c in ['+', '-', '*', '/', '^', '=', '(', ')']

expressions = [
    "A = (A^2 * (B+C)^2)",
    "B = A + C + D",
    "C = A + D^2",
    "D = (A + B)^2 + C",
    "E = (A - B + C) + (C + D^3)"
]

# Main
print("Sample: ", end="")
parse_exp("A = D - (C + B)")

print()  # Make a new line.

for i, exp in enumerate(expressions):
    print(f"{i + 1}: ", end="")
    parse_exp(exp)
