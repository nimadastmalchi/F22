# Nima Amir Dastmalchi (505320372)
# UCLA CS 131 Project 2
# Brewin++ Tokenizer

from intbase import InterpreterBase, ErrorType

# Represents a constant expression (int, bool, or string)
class Literal:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return f"{self.val} (literal)"
    
    def __repr__(self) -> str:
        return f"{self.val} (literal)"

# Represents a variable, which consists of a type and a value
class Variable:
    class Types:
        INT = int
        BOOL = bool
        STRING = str
        REFINT = InterpreterBase.REFINT_DEF
        REFBOOL = InterpreterBase.REFBOOL_DEF
        REFSTRING = InterpreterBase.REFSTRING_DEF

    # set this variable's type to type_str and set a default value according to
    # the type
    def __init__(self, type_str, referenced_var=None):
        self.type_str = type_str
        if type_str == InterpreterBase.INT_DEF:
            self.type = Variable.Types.INT
            self.value = 0
        elif type_str == InterpreterBase.BOOL_DEF:
            self.type = Variable.Types.BOOL
            self.value = False
        elif type_str == InterpreterBase.STRING_DEF:
            self.type = Variable.Types.STRING
            self.value = ""
        elif type_str == InterpreterBase.REFBOOL_DEF:
            self.type = Variable.Types.REFBOOL
        elif type_str == InterpreterBase.REFINT_DEF:
            self.type = Variable.Types.REFINT
        elif type_str == InterpreterBase.REFSTRING_DEF:
            self.type = Variable.Types.REFSTRING


# Represents a single executable line of the program
class Line:
    def __init__(self, tokens, line_number, indent):
        self.tokens = tokens
        self.line_number = line_number
        self.indent = indent

    def __str__(self):
        return f"{self.line_number}: {self.tokens}"

    def __repr__(self):
        return f"{self.__str__()}"


# Represents a scoped block in the program (while, if, or function)
class Block:
    def __init__(self, tokens, start_line, end_line, indent, outer_block):
        self.tokens = tokens
        self.start_line = start_line
        self.end_line = end_line
        self.indent = indent
        self.outer_block = outer_block
        self.variables = {}
    
    def __str__(self):
        return f"{self.tokens} ({self.start_line}:{self.end_line})"
    
    def __repr__(self) -> str:
        return self.__str__()

class IfBlock(Block):
    def __init__(self, tokens, start_line, end_line, indent, outer_block, else_line):
        super().__init__(tokens, start_line, end_line, indent, outer_block)
        self.else_line = else_line

class WhileBlock(Block):
    def __init__(self, tokens, start_line, end_line, indent, outer_block):
        super().__init__(tokens, start_line, end_line, indent, outer_block)

class FunctionBlock(Block):
    def __init__(self, tokens, start_line, end_line, indent, outer_block, params, return_type):
        super().__init__(tokens, start_line, end_line, indent, outer_block)
        self.original_params = []
        for param in params:
            self.original_params.append([param[0], Variable(param[1].type_str)])
        self.stack = []
        self.return_type = return_type

    def start_new_frame_params(self):
        params = []
        for original_param in self.original_params:
            params.append([original_param[0], Variable(original_param[1].type_str)])
        self.params = params
        self.stack.append((self.params, {}))
    
    def start_new_frame_variables(self):
        for param in self.params:
            self.stack[-1][1][param[0]] = param[1]
        self.variables = self.stack[-1][1]

    def end_frame(self):
        self.stack.pop()
        if len(self.stack) > 0:
            self.params = self.stack[-1][0]
            self.variables = self.stack[-1][1]
        else:
            self.params = None
            self.variables = None

# @param lines     - list of strings such that element i is the i-th line of the program
# @param functions - after this function call, functions maps all function names to
#                    its corresponding Function type
# @return a list of (Line | Block) representing the tokenized program
def tokenize(functions, lines):
    program = []
    for line_number, line_str in enumerate(lines):
        # represents one line of the program
        indent = len(line_str) - len(line_str.lstrip())
        line_str = line_str.strip()
        tokens = []
        i = 0
        while i < len(line_str):
            # remove all white space
            while i < len(line_str) and line_str[i] == " ":
                i += 1
            # ignore comments:
            if line_str[i] == InterpreterBase.COMMENT_DEF:
                break
            # find the end of the current token:
            j = i + 1
            if line_str[i] == '"':
                while j < len(line_str) and line_str[j] != '"':
                    j += 1
                j += 1
                token = line_str[i:j]
            else:
                while j < len(line_str) and\
                      line_str[j] != " " and\
                      line_str[j] != InterpreterBase.COMMENT_DEF:
                    j += 1
                token = line_str[i:j].strip()
            i = j

            # process literal tokens:
            if token[0] == '"':
                # string literal
                assert token[-1] == '"',\
                       'Unexpected syntax error: string literal is missing closing "'
                token = Literal(token[1:-1])
            elif is_int(token):
                # int literal
                token = Literal(int(token))
            elif token == "True":
                # bool literal
                token = Literal(True)
            elif token == "False":
                # bool literal
                token = Literal(False)
            tokens.append(token)
        program.append(Line(tokens, line_number, indent))

    # Replace Lines representing "while", "if", or "function" with the
    # appropriate types
    # keep track of current block in a stack
    blocks = [None]
    for i, line in enumerate(program):
        if len(line.tokens) > 0:
            if line.tokens[0] in {InterpreterBase.ENDFUNC_DEF,
                                  InterpreterBase.ENDIF_DEF,
                                  InterpreterBase.ENDWHILE_DEF}:
                blocks.pop()
            if line.tokens[0] == InterpreterBase.FUNC_DEF:
                return_types = {
                    'void'   : None,
                    'int'    : int,
                    'bool'   : bool,
                    'string' : str
                }
                return_type = return_types[line.tokens[-1]]

                # Form the params array
                params = []
                param_tokens = line.tokens[2:-1]
                for param_token in param_tokens:
                    param_token = param_token.split(':')
                    var_name = param_token[0]
                    type = param_token[1]
                    params.append([var_name, Variable(type)])

                # create the params array:
                # look for the end of the function:
                end_line = line.line_number + 1
                while program[end_line].indent != line.indent or\
                      len(program[end_line].tokens) == 0:
                    end_line += 1
                program[i] = FunctionBlock(line.tokens, line.line_number, end_line,\
                                   line.indent, blocks[-1], params, return_type)
                blocks.append(program[i])
                # create a variable for the function:
                functions[line.tokens[1]] = program[i]
            elif line.tokens[0] == InterpreterBase.IF_DEF:
                # find endif (and maybe else) lines
                end_line = line.line_number + 1
                else_line = None
                while True:
                    if len(program[end_line].tokens) > 0 and\
                       program[end_line].indent == line.indent:
                        if program[end_line].tokens[0] == InterpreterBase.ELSE_DEF:
                            # Ensure that this "else" is the first one
                            # encountered before an "endif" at this indentation
                            # level
                            assert else_line is None, "Unexpected syntax error"
                            else_line = end_line 
                        elif program[end_line].tokens[0] == InterpreterBase.ENDIF_DEF:
                            break
                    end_line += 1
                program[i] = IfBlock(line.tokens, line.line_number, end_line,\
                                   line.indent, blocks[-1], else_line)
                blocks.append(program[i])
            elif line.tokens[0] == InterpreterBase.WHILE_DEF:
                # look for the end of the while loop
                end_line = line.line_number + 1
                while program[end_line].indent != line.indent or\
                      len(program[end_line].tokens) == 0:
                    end_line += 1
                program[i] = WhileBlock(line.tokens, line.line_number, end_line,\
                                   line.indent, blocks[-1])
                blocks.append(program[i])
    return program


# @return True iff str represents an int
def is_int(str):
    if len(str) == 0:
        return False
    if str[0] == "+" or str[0] == "-":
        return str[1:].isdigit()
    return str.isdigit()
