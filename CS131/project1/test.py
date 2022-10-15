from re import A
from interpreterv1 import Interpreter

interpreter = Interpreter()
assert(interpreter.get_operand_value("hello") is None)
assert(interpreter.get_operand_value("\"hello\"") == "hello")
assert(interpreter.get_operand_value("10") == 10)
assert(interpreter.get_operand_value("True"))
assert(interpreter.eval_prefix_expr("+ - 20 * 3 4 1") == 9)
assert(interpreter.eval_prefix_expr("- * 3 + 3 7 / * 4 2 2") == 26)
#print(interpreter.eval_prefix_expr("- * 10 True + 10 20"))
#print(interpreter.eval_prefix_expr("| 5 2"))
assert(interpreter.eval_prefix_expr("32") == 32)
assert(interpreter.eval_prefix_expr("\"this is # a string\"") == "this is # a string")
# assert(interpreter.eval_prefix_expr("-32") == -32)
# assert(interpreter.eval_prefix_expr("> 20 32") == False)
# assert(interpreter.eval_prefix_expr("== 5 - 10 5"))
# assert(interpreter.eval_prefix_expr("& > 6 5 <= 3 3"))
# assert(interpreter.eval_prefix_expr("== \"foobar\" \"foobar\"") == True)