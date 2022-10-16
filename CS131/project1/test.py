from re import A
from interpreterv1 import Interpreter, Function

# interpreter = Interpreter()
# interpreter.run(["+ - 20 * 3 4 1",
#                 "- * 3 + 3 7 / * 4 2 2",
#                 "32",
#                 '"this is a string"',
#                 "-32",
#                 "& > 6 5 <= 3 3",
#                 "+ 1 2 # comment"])
interpreter = Interpreter()
interpreter.run(["func main",
                  "  assign x - * 3 + 3 7 / * 4 2 2",
                  "  while > x 0",
                  "    assign x - x 1",
                  "  endwhile",
                  "  assign y 10",
                  "endfunc",
                  "func hello",
                  '  funccall print "this is a string"',
                  "endfunc"])

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