from ctypes.wintypes import BOOL
from lib2to3.pgen2.tokenize import tokenize
from tarfile import SUPPORTED_TYPES
from intbase import InterpreterBase, ErrorType
import operator
import csv

# map operand type to set of supported operators
SUPPROTED_OPERATORS = {
    int: {"+", "-", "*", "/", "%", "<", ">", "<=", ">=", "!=", "=="},
    str: {"+", "==", "!=", "<", ">", "<=", ">="},
    bool: {"!=", "==", "&", "|"}
}

# map operator string to operator function
OPERATOR_MAPPING = {
    "+" : operator.add,
    "-" : operator.sub,
    "*" : operator.mul,
    "/" : operator.floordiv,
    "%" : operator.mod,
    "<" : operator.lt,
    ">" : operator.gt,
    "<=" : operator.le,
    ">=" : operator.ge,
    "!=" : operator.ne,
    "==" : operator.eq,
    "&" : operator.and_,
    "|" : operator.or_
}

# represents one line of the program
class Line:
    # Create a new Line object. This constructor will tokenize the line
    # @param line_number - the line number
    # @param line_str - a string representation of the line (untokenized)
    def __init__(self, line_number, line_str):
        self.line_number = line_number
        self.line_str = line_str
        self.indent = len(self.line_str) - len(self.line_str.lstrip())
        self.line_str = self.line_str.strip()
        self.tokenized_line = []
        i = 0
        while i < len(self.line_str):
            if self.line_str[i] == InterpreterBase.COMMENT_DEF:
                break
            # remove all white space
            while i < len(self.line_str) and self.line_str[i] == " ":
                i += 1
            j = i + 1
            if self.line_str[i] == '"':
                while j < len(self.line_str) and self.line_str[j] != '"':
                    j += 1
                token = self.line_str[i:j+1]
            else:
                while j < len(self.line_str) and self.line_str[j] != " ":
                    j += 1
                token = self.line_str[i:j].strip()
            i = j + 1

            # process token:
            if token[0] == '"':
                # string literal
                if token[-1] != '"':
                    InterpreterBase.error(ErrorType.TYPE_ERROR,
                                          f"Invalid string literal: {token}")
                token = token[1:-1]
            elif is_int(token):
                # int literal
                token = int(token)
            elif token == "True":
                # bool literal
                token = True
            elif token == "False":
                # bool literal
                token = False
            else:
                # TODO: token is a variable or key word. Do some checking
                pass
            self.tokenized_line.append(token)
    
    def __str__(self):
        return f"{self.line_number}: {self.tokenized_line}"

    def __repr__(self):
        return f"{self.__str__()}"

class Function:
    def __init__(self, start_line, tokenized_program):
        tokenized_first_line = tokenized_program[start_line].tokenized_line
        if len(tokenized_first_line) != 2:
            InterpreterBase.error(ErrorType.SYNTAX_ERROR, "Invalid function definition")
        self.start_line = start_line
        assert tokenized_first_line[0] == InterpreterBase.FUNC_DEF,\
               f"Provided start_line ({start_line}) does not define a function"
        self.func_name = tokenized_first_line[1]
        # TODO validate func_name
        i = self.start_line + 1
        while i < len(tokenized_program) and\
              tokenized_program[i].tokenized_line[0] != InterpreterBase.ENDFUNC_DEF:
            i += 1
        self.end_line = i
        # self.body = tokenized_program[self.start_line+1: self.end_line]

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, input=None, trace_output=False):
        super().__init__(console_output, input)   # call InterpreterBase’s constructor
        self.indents = []
        self.globals = {}
        self.tokenized_program = []

    def run(self, program):
        self.tokenized_program = self.tokenize(program)
        self.add_funcs_to_global()
        print(self.globals)

    def tokenize(self, program):
        tokenized_program = []
        for i, line in enumerate(program):
            tokenized_program.append(Line(i, line))
        return tokenized_program

    def add_funcs_to_global(self):
        assert self.tokenized_program is not None,\
               "call tokenize() before add_funcs_to_global()"
        for i, line in enumerate(self.tokenized_program):
            if line.tokenized_line[0] == InterpreterBase.FUNC_DEF:
                func = Function(i, self.tokenized_program)
                self.globals[func.func_name] = func

    # @param expr - a list of tokens that represent the expression
    # @return the result of the expression
    def eval_prefix_expr(self, expr):
        expr.reverse()
        stack = []
        for op in expr:
            if op not in OPERATOR_MAPPING:
                # op is an operand:
                stack.append(op)
            else:
                operand1 = stack.pop()
                operand2 = stack.pop()
                type1, type2 = type(operand1), type(operand2)
                if type1 != type2:
                    InterpreterBase.error(
                        ErrorType.TYPE_ERROR,
                        f"Expression contains operands of different types: {type1} and {type2}")
                if op not in SUPPROTED_OPERATORS[type1]:
                    Interpreter.error(
                        ErrorType.TYPE_ERROR,
                        f"Unsupported operator {op} for the operand type {type1}"
                    )
                stack.append(OPERATOR_MAPPING[op](operand1, operand2))
        if len(stack) != 1:
            InterpreterBase.error(
                ErrorType.SYNTAX_ERROR,
                f"Invalid prefix expression {expr}"
            )
        return stack[0]

# @return True iff str represents an int
def is_int(str):
    if len(str) == 0:
        return False
    if str[0] == "+" or str[0] == "-":
        return str[1:].isdigit()
    return str.isdigit()