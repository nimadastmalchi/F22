# Nima Amir Dastmalchi (505320372)
# UCLA CS 131 Project 1
# Brewin Interpreter

from intbase import InterpreterBase, ErrorType
import operator
from tokenizer import tokenize, Literal, Block

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

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, input=None, trace_output=False):
        super().__init__(console_output, input)   # call InterpreterBase’s constructor
        self.globals = {}
        self.tokenized_program = []

        # set this flag to true when return line is
        # interpreted. This will cause future instructions
        # to be no-ops
        self.current_func_terminated = False

    def run(self, program):
        self.reset() # reset the state
        self.tokenized_program = tokenize(self.globals, program)
        if "main" not in self.globals:
            # TODO figure out error type
            super().error(ErrorType.SYNTAX_ERROR,\
                          description='Could not find "main" function',
                          line_num=0)
        self.ip = self.globals["main"].start_line + 1
        # continue interpreting until we reach end of main
        while self.ip != self.globals["main"].end_line:
            self.interpret()

    def interpret(self):
        #print(str(self.ip) + ":", self.tokenized_program[self.ip].line_str)
        tokens = self.tokenized_program[self.ip].tokens
        cur_indent = self.tokenized_program[self.ip].indent
        if self.current_func_terminated:
            pass
        elif len(tokens) == 0 or\
           tokens[0] in [InterpreterBase.ENDFUNC_DEF, InterpreterBase.ENDWHILE_DEF, InterpreterBase.ENDIF_DEF]:
            pass
        elif tokens[0] == InterpreterBase.ASSIGN_DEF:
            var_name = tokens[1]
            var_value = self.eval_prefix_expr(tokens[2:])
            self.globals[var_name] = var_value
        elif tokens[0] == InterpreterBase.FUNCCALL_DEF:
            func_name = tokens[1]
            if func_name == InterpreterBase.INPUT_DEF:
                self.built_in_input(tokens[2:])
            elif func_name == InterpreterBase.PRINT_DEF:
                self.built_in_print(tokens[2:])
            elif func_name == InterpreterBase.STRTOINT_DEF:
                self.built_in_strtoint(tokens[2:])
            else:
                func = self.globals[func_name]
                if type(func) is not Block or func.type != Block.Types.FUNCTION:
                    # TODO check error type
                    super().error(ErrorType.NAME_ERROR,
                                  f"{func_name} is not a function",
                                  self.ip)
                # store current line in lr before function call:
                lr = self.ip
                # evaluate the function:
                self.ip = func.start_line + 1
                while self.ip != func.end_line:
                    self.interpret()
                # set self.ip to address to return to:
                self.ip = lr
                self.current_func_terminated = False
        elif tokens[0] == InterpreterBase.WHILE_DEF:
            start_line = self.tokenized_program[self.ip].start_line
            end_line = self.tokenized_program[self.ip].end_line
            # evaluate the while loop
            while self.eval_prefix_expr(tokens[1:]):
                self.ip += 1 # skip the "while" statement
                while self.ip != end_line:
                    # recursively interpret each line
                    self.interpret()
                self.ip = start_line
            self.ip = end_line
        elif tokens[0] == InterpreterBase.RETURN_DEF:
            if len(tokens) > 1:
                # Evaluate the expression being returned and set it to the
                # "result" global variable:
                return_val = self.eval_prefix_expr(tokens[1:])
                self.globals[InterpreterBase.RESULT_DEF] = return_val
            self.current_func_terminated = True
            return
        elif tokens[0] == InterpreterBase.IF_DEF:
            if len(tokens) <= 1:
                super().error(\
                    ErrorType.SYNTAX_ERROR,\
                    description='Expected expression after "if"',\
                    line_num=self.ip\
                )
            start_line = self.tokenized_program[self.ip].start_line
            end_line = self.tokenized_program[self.ip].end_line
            else_line = self.tokenized_program[self.ip].else_line

            # evaluate the if expression
            if_expr_value = self.eval_prefix_expr(tokens[1:])
            if_expr_type = type(if_expr_value)
            if if_expr_type is not bool:
                super().error(\
                    ErrorType.TYPE_ERROR,\
                    description="Expecting boolean expression in if statement",\
                    line_num=self.ip
                    )
            if if_expr_value:
                cur_end_line = else_line if else_line is not None else end_line
                self.ip += 1
                while self.ip != cur_end_line:
                    self.interpret()
            elif else_line is not None:
                self.ip = else_line + 1
                while self.ip != end_line:
                    self.interpret()
            self.ip = end_line
        else:
            super().error(ErrorType.SYNTAX_ERROR,\
                          description="Unkown line",
                          line_num=self.ip)
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
                        ErrorType.TYPE_ERROR,\
                        description=f"Expression contains operands of different types: {type1} and {type2}",\
                        line_num=self.ip)
                if op not in SUPPROTED_OPERATORS[type1]:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f"Unsupported operator {op} for the operand type {type1}"
                    )
                stack.append(OPERATOR_MAPPING[op](operand1, operand2))
            else:
                # a variable
                if op not in self.globals:
                    super().error(ErrorType.NAME_ERROR,\
                                  description=f"Undefined variable {op}",\
                                  line_num=self.ip)
                else:
                    stack.append(self.globals[op])
        if len(stack) != 1:
            super().error(
                ErrorType.SYNTAX_ERROR,
                f"Invalid prefix expression {expr}"
            )
        return stack[0]

    def reset(self):
        super().reset()
        self.tokenized_program = []
        self.globals = {}

    def built_in_input(self, args):
        concat_string = ""
        for arg in args:
            if type(arg) is Literal and type(arg.val) is str:
                concat_string += arg.val
            elif arg in self.globals and type(self.globals[arg]) is str:
                concat_string += self.globals[arg]
            else:
                # TODO check
                super().error(ErrorType.SYNTAX_ERROR,\
                              description='Invalid argument(s) to function "input"',\
                              line_num=self.ip)
        super().output(concat_string)
        self.globals[InterpreterBase.RESULT_DEF] = super().get_input()

    def built_in_print(self, args):
        concat_string = ""
        for arg in args:
            if type(arg) is Literal:
                concat_string += str(arg.val)
            elif arg in self.globals:
                concat_string += str(self.globals[arg])
            else:
                # TODO check
                # TODO do a NAME_ERROR if arg is an undefined variable
                super().error(ErrorType.SYNTAX_ERROR,\
                              description='Invalid argument(s) to function "print"',\
                              line_num=self.ip)
        super().output(concat_string)

    def built_in_strtoint(self, args):
        if len(args) != 1:
            super().error(\
                ErrorType.SYNTAX_ERROR,\
                description=f'Expected 1 argument to "strtoint" but got {len(args)}',
                line_num=self.ip)
        val = None
        if type(args[0]) is Literal:
            if type(args[0].val) is not str:
                super().error(\
                    ErrorType.TYPE_ERROR,\
                    description=f'Expected a string literal but got a non-string literal as argument to "strtoint"',\
                    line_num=self.ip)
            val = args[0].val
        elif args[0] in self.globals:
            val = self.globals[args[0]]
        else:
            super().error(\
                ErrorType.NAME_ERROR,\
                description=f"Undefined variable {args[0]}",\
                line_num=self.ip)
        try:
            converted_int = int(val)
            self.globals[InterpreterBase.RESULT_DEF] = converted_int
        except:
            super().error(\
                ErrorType.TYPE_ERROR,\
                description=f'Provided string "{val}" cannot be converted to int',\
                line_num=self.ip)


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
