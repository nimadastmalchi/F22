# Nima Amir Dastmalchi (505320372)
# UCLA CS 131 Project 1
# Brewin Interpreter

from configparser import InterpolationError
from intbase import InterpreterBase, ErrorType
import operator

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

# all keywords of the language
KEY_WORDS = {
    InterpreterBase.FUNC_DEF,
    InterpreterBase.ENDFUNC_DEF,
    InterpreterBase.ASSIGN_DEF,
    InterpreterBase.FUNCCALL_DEF
}

class Literal:
    def __init__(self, val):
        self.val = val
    
    def __str__(self):
        return f"{self.val}"
    
    def __repr__(self) -> str:
        return f"{self.val}"

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
                    super().error(ErrorType.TYPE_ERROR,
                                          f"Invalid string literal: {token}")
                token = token[1:-1]
            elif is_int(token):
                # int literal
                token = Literal(int(token))
            elif token == "True":
                # bool literal
                token = Literal(True)
            elif token == "False":
                # bool literal
                token = Literal(False)
            self.tokenized_line.append(token)

    def __str__(self):
        return f"{self.line_number}: {self.tokenized_line}"

    def __repr__(self):
        return f"{self.__str__()}"

class Function:
    def __init__(self, start_line, end_line):
        self.start_line = start_line
        self.end_line = end_line

    def __str__(self):
        return f"Function ({self.start_line}:{self.end_line})"

    def __repr__(self):
        return f"{self.__str__()}"

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, input=None, trace_output=False):
        super().__init__(console_output, input)   # call InterpreterBase’s constructor
        self.globals = {}
        self.tokenized_program = []

    def run(self, program):
        self.reset() # reset the state
        self.tokenize(program)
        self.add_funcs_to_global()
        if "main" not in self.globals:
            # TODO figure out error type
            super().error(ErrorType.TYPE_ERROR,
                                  'Could not find "main" function')
        self.ip = self.globals["main"].start_line + 1
        # continue interpreting until we reach end of main
        while self.ip != self.globals["main"].end_line:
            self.interpret()
        print(self.globals)

    def tokenize(self, program):
        self.tokenized_program = []
        for i, line in enumerate(program):
            self.tokenized_program.append(Line(i, line))

    def add_funcs_to_global(self):
        assert self.tokenized_program is not None,\
               "call tokenize() before add_funcs_to_global()"
        for i, line in enumerate(self.tokenized_program):
            if line.tokenized_line[0] == InterpreterBase.FUNC_DEF:
                func_name = line.tokenized_line[1]
                j = i + 1
                while len(self.tokenized_program[j].tokenized_line) == 0 or\
                      self.tokenized_program[j].tokenized_line[0] != InterpreterBase.ENDFUNC_DEF:
                    j += 1
                self.globals[func_name] = Function(i, j)

    def interpret(self):
        print(self.tokenized_program[self.ip].line_str)
        line = self.tokenized_program[self.ip].tokenized_line
        cur_indent = self.tokenized_program[self.ip].indent
        if line == "" or\
           line[0] in [InterpreterBase.ENDFUNC_DEF, InterpreterBase.ENDWHILE_DEF, InterpreterBase.ENDIF_DEF]:
            pass
        elif line[0] == InterpreterBase.ASSIGN_DEF:
            var_name = line[1]
            var_value = self.eval_prefix_expr(line[2:])
            self.globals[var_name] = var_value
        elif line[0] == InterpreterBase.FUNCCALL_DEF:
            func_name = line[1]
            func = self.globals[func_name]
            if type(func) is not Function:
                # TODO check error type
                super().error(ErrorType.NAME_ERROR,
                                    f"{func_name} is not a function")
            # store current line in lr before function call:
            lr = self.ip
            # evaluate the function:
            self.ip = func.start_line + 1
            while self.ip != func.end_line:
                self.interpret()
            # set self.ip to address to return to:
            self.ip = lr
        elif line[0] == InterpreterBase.WHILE_DEF:
            # store start and end lines of the while block
            start_line = self.ip
            end_line = self.ip + 1
            while self.tokenized_program[end_line].indent != cur_indent:
                end_line += 1
            tokenized_end_line = self.tokenized_program[end_line].tokenized_line
            if len(tokenized_end_line) != 1 or\
               tokenized_end_line[0] != InterpreterBase.ENDWHILE_DEF:
                super().error(\
                    ErrorType.SYNTAX_ERROR,\
                    description='Expected "endwhile" after "while"',\
                    line_num=end_line)
            # evaluate the while loop
            while self.eval_prefix_expr(line[1:]):
                self.ip += 1 # skip the "while" statement
                while self.ip != end_line:
                    # recursively interpret each line
                    self.interpret()
                self.ip = start_line
            self.ip = end_line
        elif line[0] == InterpreterBase.RETURN_DEF:
            if len(line) > 1:
                # Evaluate the expression being returned and set it to the
                # "result" global variable:
                return_val = self.eval_prefix_expr(line[1:])
                self.globals[InterpreterBase.RESULT_DEF] = return_val
                # set ip to the "endfunc" line
                # TODO we already store end_line, so use it from the Function struct somehow
                end_line = self.ip + 1
                # no nested functions, so we can safely look for next endfunc
                while len(self.tokenized_program[end_line].tokenized_line) == 0 or\
                      self.tokenized_program[end_line].tokenized_line[0] != InterpreterBase.ENDFUNC_DEF:
                    end_line += 1
                self.ip = end_line
                return
        elif line[0] == InterpreterBase.IF_DEF:
            if len(line) <= 1:
                super().error(\
                    ErrorType.SYNTAX_ERROR,\
                    description='Expected expression after "if"',\
                    line_num=self.ip\
                )
            # find endif (and else) lines
            i = self.ip + 1
            else_line = None
            end_if_line = None
            while True:
                cur_line = self.tokenized_program[i].tokenized_line
                if len(cur_line) > 0:
                    if self.tokenized_program[i].indent == cur_indent:
                        if cur_line[0] == InterpreterBase.ELSE_DEF:
                            if else_line is not None:
                                super().error(\
                                    ErrorType.SYNTAX_ERROR,\
                                    description='Unexpected "else"',\
                                    line_num=i\
                                )
                            else_line = i
                        elif cur_line[0] == InterpreterBase.ENDIF_DEF:
                            end_if_line = i
                            break
                i += 1
            
            # evaluate the if expression
            if_expr_value = self.eval_prefix_expr(line[1:])
            if_expr_type = type(if_expr_value)
            if if_expr_type is not bool:
                super().error(\
                    ErrorType.TYPE_ERROR,\
                    description="Expecting boolean expression in if statement",\
                    line_num=self.ip
                    )
            if if_expr_value:
                end_line = else_line if else_line is not None else end_if_line
                self.ip += 1
                while self.ip != end_line:
                    self.interpret()
            elif else_line is not None:
                self.ip = else_line + 1
                while self.ip != end_if_line:
                    self.interpret()
            self.ip = end_if_line
        else:
            # TODO error name
            super().error(ErrorType.SYNTAX_ERROR,
                                  f"Unkown line")
        self.ip += 1

    # @param expr - a list of tokens that represent the expression
    # @return the result of the expression
    def eval_prefix_expr(self, expr):
        expr.reverse()
        stack = []
        for op in expr:
            if type(op) is Literal:
                stack.append(op.val)
            elif op in OPERATOR_MAPPING:
                operand1 = stack.pop()
                operand2 = stack.pop()
                type1, type2 = type(operand1), type(operand2)
                if type1 != type2:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f"Expression contains operands of different types: {type1} and {type2}")
                if op not in SUPPROTED_OPERATORS[type1]:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f"Unsupported operator {op} for the operand type {type1}"
                    )
                stack.append(OPERATOR_MAPPING[op](operand1, operand2))
            else:
                # a variable
                if op not in self.globals:
                    super().error(ErrorType.NAME_ERROR,
                                          f"Undefined variable {op}")
                else:
                    stack.append(self.globals[op])
        if len(stack) != 1:
            super().error(
                ErrorType.SYNTAX_ERROR,
                f"Invalid prefix expression {expr}"
            )
        return stack[0]

    def reset(self):
        self.tokenized_program = []
        self.globals = {}

# @return True iff str represents an int
def is_int(str):
    if len(str) == 0:
        return False
    if str[0] == "+" or str[0] == "-":
        return str[1:].isdigit()
    return str.isdigit()

# @return True iff name is a valid variable name
def is_valid_var_name(name):
    if len(name) == 0:
        return False
    # ensure first character is a letter
    if not name[0].isalpha():
        return False
    # expecting all other characters to be letters, digit, or underscore
    for i in range(1, len(name)):
        if not (name[i].isalpha() or name[i].isdigit() or name[i] == "_"):
            return False
    return True
