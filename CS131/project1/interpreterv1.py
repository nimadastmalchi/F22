from ctypes.wintypes import BOOL
from tarfile import SUPPORTED_TYPES
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

class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, input=None, trace_output=False):
        super().__init__(console_output, input)   # call InterpreterBase’s constructor
        self.global_ = {}

    def run(self, program):
        pass

    # @param expr - a string representing a prefix expression to evaluate
    # @return the result of the expression
    def eval_prefix_expr(self, expr : str):
        # get list of operands and operators:
        # TODO: Change this to a tokenizer that works for strings with spaces
        ops = expr.split(' ')
        ops.reverse()

        stack = []
        for op in ops:
            if op not in OPERATOR_MAPPING:
                # op is an operand:
                stack.append(self.get_operand_value(op))
            else:
                operand1 = stack.pop()
                operand2 = stack.pop()
                type1, type2 = type(operand1), type(operand2)
                if type(operand1) != type(operand2):
                    InterpreterBase.error(
                        ErrorType.TYPE_ERROR,
                        f"Expression contains operands of different types: {type1} and {type2}")
                if op not in SUPPROTED_OPERATORS[type(operand1)]:
                    Interpreter.error(
                        ErrorType.TYPE_ERROR,
                        f"Unsupported operator {op} for the operand type {type1}"
                    )
                stack.append(OPERATOR_MAPPING[op](operand1, operand2))
        if len(stack) != 1:
            InterpreterBase.error(
                ErrorType.SYNTAX_ERROR,
                f"Invalid prefix expression"
            )
        return stack[0]

    # @param op - an operand (a string variable name or an operand represented
    #   as a string (e.g., "\"hello\"", "10", "True"))
    # @return the value of the operand (int, str, or bool). Return None if the
    #   operand does not have a value (e.g., undefined variable name)
    def get_operand_value(self, op):
        if op in self.global_:
            return self.global_[op]
        if op[0] == "\"":
            if op[len(op) - 1] != "\"":
                return None # invalid str
            return op[1:len(op)-1]
        if op == "True":
            return True
        if op == "False":
            return False
        try:
            return int(op)
        except:
            # TODO: handle unknown operand case (this could be an undefined variable)
            return None

