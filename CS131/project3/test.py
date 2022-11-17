from re import A
from interpreterv3 import Interpreter

f = open('input.txt')
program = []
for line in f:
    if len(line) > 0 and line[-1] == '\n':
        line = line[:-1]
    program.append(line)
interpreter = Interpreter()
interpreter.run(program)
# globals = {}
# interpreter.run(["func main",
#                  "  assign x 10",
#                  "  funccall main2",
#                  '  funccall print \"hello world\"',
#                  "endfunc",
#                  "func main2",
#                  "  return",
#                  "endfunc"])
# print(interpreter.globals)
# interpreter.run(["func main",
#                  "  assign  y   10",
#                  "  funccall   main2",
#                  "endfunc",
#                  "func main2",
#                  "  return",
#                  "  assign should_not_be_assigned 10",
#                  "endfunc"])
# print(interpreter.globals)
# print(tokenize(
#     globals,
#     ["func main",
#      "  assign n 5",
#      '  assign f 1 "hello"',
#      "  funccall fact",
#      "endfunc",
#      "func fact",
#      "  if == n 0",
#      "    return f", # bug: if expression will execute until self.ip gets to endif. return will put self.ip to endfunc. So, self.ip increments to after length of program
#      "  endif",
#      "  assign f * f n",
#      "  assign n - n 1",
#      "  funccall fact",
#      "  return result",
#      "endfunc",
#     ]
# ))

# interpreter.run(
#     ["func even",
#      "  if == n 0",
#      "      return True",
#      "  endif",
#      "  assign n - n 1",
#      "  funccall odd",
#      "  return result",
#      "endfunc",

#     "func odd",
#     "    if == n 0",
#     "        return False",
#     "    endif",
#     "    assign n - n 1",
#     "    funccall even",
#     "    return result",
#     "endfunc",

#     "func isEven",
#     "   funccall even",
#     "   if == result True",
#     '       funccall print "number is even"',
#     "   else",
#     '       funccall print "number is odd"',
#     "   endif",
#     "endfunc",

#     "func main",
#     "   assign n 15",
#     "   funccall isEven",
#     "   assign n 20",
#     "   funccall isEven",
#     "   assign n 0",
#     "   funccall isEven",
#     "   assign n 548",
#     "   funccall isEven",
#     "endfunc",
# ]
# )

# interpreter.run(
#     ["func main",
#      "  assign n 5",
#      '  assign f 1',
#      "  funccall fact",
#      "endfunc",
#      "func fact",
#      "  if == n 0",
#      "    return f", # bug: if expression will execute until self.ip gets to endif. return will put self.ip to endfunc. So, self.ip increments to after length of program
#      "  endif",
#      "  assign f * f n",
#      "  assign n - n 1",
#      "  funccall fact",
#      "  return result",
#      "endfunc",
#     ]
# )

# strtoint test
# interpreter.run(["func main",
#                   '  assign v1 20',
#                   '  funccall print v1',
#                   "endfunc"])

# interpreter.run(["func main",
#                   '  assign x "please"',
#                   '  funccall input "Enter your name " x ":"',
#                   '  funccall print "Hello, " result',
#                   "endfunc"])

# interpreter.run(["func main",
#                   "  assign x - * 3 + 3 7 / * 4 2 2",
#                   "  while > x 0",
#                   "    assign x - x 1",
#                   "    assign z 10",
#                   "    while > z 0",
#                   "       assign z - z 1",
#                   "    endwhile",
#                   "  endwhile",
#                   "  assign y 10",
#                   "  funccall hello",
#                   "  if > 1 2",
#                   "    assign fail1 10",
#                   "  else",
#                   "     assign succ1 10",
#                   "  endif",
#                   "endfunc",
#                   "func hello",
#                   '  assign a 20',
#                   "  return + a 30",
#                   "  assign b 10",
#                   "endfunc"])

# tokens = interpreter.tokenize(["+ - 20 * 3 4 1 1h",
#                 "- * 3 + 3 7 / * 4 2 2",
#                 "32",
#                 '"this is a string"',
#                 "-32",
#                 "& > 6 5 <= 3 3",
#                 "+ 1 2 # comment"])
# print(interpreter.eval_prefix_expr(tokens[0].tokenized_line))

# assert(interpreter.eval_prefix_expr("+ - 20 * 3 4 1") == 9)
# assert(interpreter.eval_prefix_expr("- * 3 + 3 7 / * 4 2 2") == 26)
#print(interpreter.eval_prefix_expr("- * 10 True + 10 20"))
#print(interpreter.eval_prefix_expr("| 5 2"))
# assert(interpreter.eval_prefix_expr("32") == 32)
# assert(interpreter.eval_prefix_expr("\"this is # a string\"") == "this is # a string")
# assert(interpreter.eval_prefix_expr("-32") == -32)
# assert(interpreter.eval_prefix_expr("> 20 32") == False)
# assert(interpreter.eval_prefix_expr("== 5 - 10 5"))
# assert(interpreter.eval_prefix_expr("& > 6 5 <= 3 3"))
# assert(interpreter.eval_prefix_expr("== \"foobar\" \"foobar\"") == True)