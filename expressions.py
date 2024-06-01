# ANDREA TONELLO SM3201234

class EmptyStackException(Exception):
    pass

class MissingVariableException(Exception):
    pass

class NotExpressionException(Exception):
    pass

class NotArrayException(Exception):
    pass

class NotVariableException(NotExpressionException):
    pass

class SubroutineError(Exception):
    pass


class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[0:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])
    

# Returns True if n is a real number
def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


# Checks if a number n is an integer, avoiding the flattening that Python applies by default to floats when converting them to ints
def integer_check(n):

    if isinstance(n, int):                                                      # if n is already an integer:    keep n as it is
        return n
    elif isinstance(n, float) and n.is_integer():                               # if n is an integer but represented as a float:    convert n to integer 
        return int(n)
    else:                                                                       # if n is not an integer:    error
        raise TypeError(f"The index you selected (== {n}) is not an integer!")


class Expression:
    """
    Represents a mathematical expression or a generic operation.
    """
    def __init__(self):
        raise NotImplementedError()

    @classmethod
    def from_program(cls, text, dispatch):
        """
        Returns, using a stack, either one of the three basic Expressions:
        Variable, Constant or Operation
        """
        stack = Stack()
        sentence = text.split()

        for item in sentence:
        
            # if we recognize a valid operation symbol:
            if item in dispatch:                    
                
                # Create the appropriate Operation instance
                cls = dispatch[item]
                
                # Extract the required operands and pass them to the Operation instance just created
                args = []
                for _ in range(cls.arity):      # arity: number of operands in an operation
                    args.append(stack.pop())
                stack.push(cls(*args))

            # instead if we recognize a real number: create the appropriate Constant instance
            elif is_number(item):
                stack.push(Constant(float(item)))
            
            # else we are left with a string, that we interpret as a Variable instance
            else:
                stack.push(Variable(item))

        return stack.pop()

    def evaluate(self, env):
        raise NotImplementedError()


class Variable(Expression):
    """
    Represents a Variable, e.g. x, hello, etc.
    """
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):

        if self.name not in env:
            raise MissingVariableException(f"Cannot find variable {self.name} in the environment")
        return env[self.name]

    def __str__(self):
        return self.name


class Constant(Expression):
    """
    Represents a real Constant, e.g. 4, 7.2, etc.
    """
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

    def __str__(self):
        return str(self.value)


class Operation(Expression):
    """
    Represents a generic operation, e.g addition, multiplication, and also programming constructs. Must be implemented separately.
    """
    # Identifier for the selected operation
    op_symbol = None

    # Operation arguments as a list, e.g. [x,y] for the operation x + y
    def __init__(self, args: list):
        self.args = args

    def evaluate(self, env: dict):

        # Evaluates the operation's arguments based on the assignments specified in the env dictionary (if a Variable), e.g. env = {"x": 3} ...
        evaluated = []
        for arg in self.args:

            if not isinstance(arg, Expression):
                raise NotExpressionException(f"Operand {arg} is not an Expression object and it cannot be processed.")

            evaluated.append(arg.evaluate(env))

        # ...and returns the result of the corresponding operation
        return self.op(*evaluated)

    def op(self, *args):
        raise NotImplementedError()

    def __str__(self):
        return f"({self.op_symbol} {' '.join(map(str, self.args))})"



# Unary, Binary, Ternary, Quaternary operations: different arity, same construction
# -------------------------------------------------------------------------------------------------------------------------------------------

class UnaryOp(Operation):
    arity = 1

    def __init__(self, x):
        super().__init__([x])

    def op(self, x):
        raise NotImplementedError()
    

class BinaryOp(Operation):
    arity = 2

    def __init__(self, x, y):
        super().__init__([x, y])

    def op(self, x, y):
        raise NotImplementedError()
    

class TernaryOp(Operation):
    arity = 3

    def __init__(self, x, y, z):
        super().__init__([x, y, z])

    def op(self, x, y, z):
        raise NotImplementedError()
    

class QuaternaryOp(Operation):
    arity = 4

    def __init__(self, x, y, z, w):
        super().__init__([x, y, z, w])

    def op(self, x, y, z, w):
        raise NotImplementedError()



# A set of classic mathematical operations, either unary or binary
# -------------------------------------------------------------------------------------------------------------------------------------------
    
class Addition(BinaryOp):
    """
    Syntax: y x +
    """
    op_symbol = "+"
    def op(self, x, y):
        return x + y

class Subtraction(BinaryOp):
    """
    Syntax: y x -
    """
    op_symbol = "-"
    def op(self, x, y):
        return x - y
    
class Multiplication(BinaryOp):
    """
    Syntax: y x *
    """
    op_symbol = "*"
    def op(self, x, y):
        return x * y

class Division(BinaryOp):
    """
    Syntax: y x /
    """
    op_symbol = "/"
    def op(self, x, y):
        if y == 0:
            raise ZeroDivisionError("Division by zero is undefined.")
        return x / y

class Power(BinaryOp):
    """
    Syntax: y x **
    """
    op_symbol = "**"
    def op(self, x, y):
        return x ** y

class Modulus(BinaryOp):
    """
    Syntax: y x %
    """
    op_symbol = "%"
    def op(self, x, y):
        if y == 0:
            raise ValueError("Modulus by zero is undefined.")
        return x % y

class Reciprocal(UnaryOp):
    """
    Syntax: x 1/
    """
    op_symbol = "1/"
    def op(self, x):
        if x == 0:
            raise ValueError("Reciprocal of zero is undefined.")
        return 1 / x

class AbsoluteValue(UnaryOp):
    """
    Syntax: x abs
    """
    op_symbol = "abs"
    def op(self, x):
        return abs(x)
    


# A set of comparison operators
# -------------------------------------------------------------------------------------------------------------------------------------------
    
class IsEqual(BinaryOp):
    """
    Syntax: y x =
    """
    op_symbol = "="
    def op(self, x, y):
        return x == y

class IsNotEqual(BinaryOp):
    """
    Syntax: y x !=
    """
    op_symbol = "!="
    def op(self, x, y):
        return x != y

class GreaterThan(BinaryOp):
    """
    Syntax: y x >
    """
    op_symbol = ">"
    def op(self, x, y):
        return x > y
    
class GreaterEqualThan(BinaryOp):
    """
    Syntax: y x >=
    """
    op_symbol = ">="
    def op(self, x, y):
        return x >= y

class LessThan(BinaryOp):
    """
    Syntax: y x <
    """
    op_symbol = "<"
    def op(self, x, y):
        return x < y

class LessEqualThan(BinaryOp):
    """
    Syntax: y x <=
    """
    op_symbol = "<="
    def op(self, x, y):
        return x <= y
    


# Variable definition and allocation
# -------------------------------------------------------------------------------------------------------------------------------------------
       
class Alloc(UnaryOp):
    """
    Syntax: x alloc
    Initializes and allocates a variable x in the environment with the default value of 0.
    """
    op_symbol = "alloc"

    def evaluate(self, env):
        try:
            env.update({self.args[0].name: 0})
        except:
            raise NotVariableException("Only Variable objects can be allocated.")
        

class VAlloc(BinaryOp):
    """
    Syntax: n arr valloc
    Initializes and allocates an array arr of n zeros in the environment.
    """
    op_symbol = "valloc"

    def evaluate(self, env):

        # n array valloc means that valloc has two arguments, n and array.
        # However, keep in mind that we access them in a reverse order, so array is the first operand, and n is the second operand

        # evaluate n and check if it is a positive integer
        n = self.args[1].evaluate(env)
        n = integer_check(n)
        
        if n < 0:
            raise ValueError(f"The index n = {n} must be a positive integer!")
        
        # create the array
        v = [0 for _ in range(n)]
        try:
            env.update({self.args[0].name: v})
        except:
            raise NotVariableException("Only Variable objects can be allocated.")


class SetQ(BinaryOp):
    """
    Syntax: expr x setq
    Sets a variable x to a desired value, which can be the result of another expression expr.
    """
    op_symbol = "setq"

    def evaluate(self, env):

        # evaluate the expression and update the environment accordingly
        expr = self.args[1].evaluate(env)
        env.update({self.args[0].name: expr})
        x = self.args[0].evaluate(env)
        return x


class SetV(TernaryOp):
    """
    Syntax: expr n array setv
    Sets the n-th value of the array arr to the value of the expression expr.
    """
    op_symbol = "setv"

    def evaluate(self, env):

        # evaluate the expression and the index n, checking the validity of the latter
        expr = self.args[2].evaluate(env)
        n = self.args[1].evaluate(env)
        
        n = integer_check(n)
        
        # even though Python allows negative indexes, I wanted to simplify the logic
        if n < 0:
            raise ValueError(f"The index n = {n} must be a positive integer!")
        
        # evaluate x and check that it is in fact an array
        x = self.args[0].evaluate(env)
        
        if not isinstance(x, list):
            raise NotArrayException(f"{x} is not an array (list)")
        
        if len(x) <= n:
            raise IndexError("The index n cannot exceed the array's length")
        
        # substitute the new value
        x[n] = expr
        return x



# Sequences of operations
# -------------------------------------------------------------------------------------------------------------------------------------------
            
class Prog2(BinaryOp):
    """
    Syntax: expr1 expr2 prog2
    Evaluates two expressions and returns the final value in the first one.
    """
    op_symbol = "prog2"
    
    def evaluate(self, env):

        self.args[0].evaluate(env)
        return self.args[1].evaluate(env)
    

class Prog3(TernaryOp):
    """
    Syntax: expr1 expr2 expr3 prog3
    Evaluates three expressions and returns the final value in the first one.
    """
    op_symbol = "prog3"
    
    def evaluate(self, env):

        self.args[0].evaluate(env)
        self.args[1].evaluate(env)
        return self.args[2].evaluate(env)
    

class Prog4(QuaternaryOp):
    """
    Syntax: expr1 expr2 expr3 expr4 prog4
    Evaluates four expressions and returns the final value in the first one.
    """
    op_symbol = "prog4"
    
    def evaluate(self, env):

        self.args[0].evaluate(env)
        self.args[1].evaluate(env)
        self.args[2].evaluate(env)
        return self.args[3].evaluate(env)



# Basic programming constructs: if, while, for
# -------------------------------------------------------------------------------------------------------------------------------------------

class If(TernaryOp):
    """
    Syntax: if-no if-yes cond if
    Evaluates condition cond: if True, evaluates the expression in if-yes, otherwise evaluates the expression in if-no
    """
    op_symbol = "if"

    def evaluate(self, env):

        cond = self.args[0].evaluate(env)

        if not isinstance(cond, bool):
            raise TypeError("Condition must be either True or False")

        if cond == True:
            return self.args[1].evaluate(env)       # if_yes
        elif cond == False:
            return self.args[2].evaluate(env)       # if_no

        
class While(BinaryOp):
    """
    Syntax: expr cond while
    Evaluates condition cond, and while it remains True, evaluates the expression expr
    """
    op_symbol = "while"

    def evaluate(self, env):
        
        cond = self.args[0]
        expr = self.args[1]

        # The condition must be a boolean
        if not isinstance(cond.evaluate(env), bool):
            raise TypeError("Condition must be either True or False")

        # While the condition is true, evaluate the expression
        while cond.evaluate(env):
            expr = self.args[1].evaluate(env)

        return expr


class For(QuaternaryOp):
    """
    Syntax: expr end start i for
    Evaluates expression expr i times, with the value of i that goes from start to end. The value of i can be used by expr at each iteration.
    """
    op_symbol = "for"
            
    def evaluate(self, env):
        
        # i must be a variable
        i = self.args[0]
        if not isinstance(i, Variable):
            raise NotVariableException("The index must be a variable, for example i.")
        
        # start and end must be integers; 
        # They can be negative or even inverted (--> end < start), since we need to account for all possibilities
        start = self.args[1].evaluate(env)
        end = self.args[2].evaluate(env)
        start = integer_check(start)
        end = integer_check(end)

        expr = self.args[3]

        for j in range(start, end):

            # Updating the environment with the current value of i, which may be used by expr
            env.update({i.name: j})
            expr = self.args[3].evaluate(env)

        return expr



# Subroutines: "saving" a non-evaluated expression to a variable to be called later
# -------------------------------------------------------------------------------------------------------------------------------------------

class Defsub(BinaryOp):
    """
    Syntax: expr f defsub
    Assigns expression expr to variable f, without evaluating expr, and adds f to the environment.
    """
    op_symbol = "defsub"

    def evaluate(self, env):

        try:
            f = self.args[0].name
        except:
            raise NotVariableException("The subroutine must be stored in a Variable object.")
        
        not_eval_expr = self.args[1]

        # Instead of just adding f, we also "flag" it to specify that it was generated by defsub
        env.update({f: [not_eval_expr, "_from_defsub"]})


class Call(UnaryOp):
    """
    Syntax: f call
    "Calls" f, evaluating the information stored inside it by defsub
    """
    op_symbol = "call"

    def evaluate(self, env):
        
        f = self.args[0].evaluate(env)

        # We need to verify that f comes from defsub; two steps:
        
        # - check if f is a list of length 2 (as seen in class Defsub)
        if not isinstance(f, list) or len(f) != 2:
            raise SubroutineError("Can only call expressions defined by defsub!")
        
        # - since f might be an arbitrary array, e.g. [0,0] created by valloc, we check the presence of the flag "_from_defsub"
        if f[1] != "_from_defsub":
            raise SubroutineError("Can only call expressions defined by defsub!")

        # We evaluate the first item of f, which is the expression
        return f[0].evaluate(env)
    


# Additional utilities: print, null-operation
# -------------------------------------------------------------------------------------------------------------------------------------------

class Print(UnaryOp):
    """
    Syntax: expr print
    Evaluates and prints expression expr.
    """
    op_symbol = "print"

    def evaluate(self, env):
        
        expr = self.args[0].evaluate(env)
        print(expr)
        return expr


class NullaryOp(Operation):
    """
    Syntax: nop
    A special class representing the null-ary operation.
    """
    op_symbol = "nop"
    arity = 0

    def __init__(self):
        pass

    def evaluate(self, env):
        return "No OP"

    def op(self, *args):
        pass

    def __str__(self):
        return f"({self.op_symbol})"



# Arguments and operations dictionary
    
d = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction, "/": Division, "%": Modulus, "1/": Reciprocal, "abs": AbsoluteValue,
     "=": IsEqual, "!=": IsNotEqual, ">": GreaterThan, ">=": GreaterEqualThan, "<": LessThan, "<=": LessEqualThan,
     "alloc": Alloc, "valloc": VAlloc, "setq": SetQ, "setv": SetV, "prog2": Prog2, "prog3": Prog3, "prog4": Prog4,
     "if": If, "while": While, "for": For, "defsub": Defsub, "call": Call, "print": Print, "nop": NullaryOp}


# Leaving the main as a comment, maybe it turns out to be useful during the correction

'''ex1 = "2 3 + x * 6 -"
ex2 = "2 3 + x * 6 5 - / abs 2 ** y 1/ + 1/"
ex3 = "x 4.3 >"
ex4 = "2 x + 4 x - x setq x alloc prog3"
ex5 = "4 y valloc"

ex6 = "4 x setq"
ex7 = "4.2 6 y setv"
ex8 = "5 2 x setv"
ex9 = "nop x 4 + 5 x = if 5 x setq x alloc prog3"
ex10 = "x 1 + x setq x 10 > while x alloc prog2"

ex11 = "v print i i * i v setv prog2 10 0 i for 10 v valloc prog2"
ex12 = "x print f call x alloc x 4 + x setq f defsub prog4"
ex13 = "nop i print i x % 0 = if 1000 2 i for 783 x setq x alloc prog3"
ex14 = "nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for"
ex15 = "5 print x 10 > while"

ex16 = "v print i j * 1 i - 10 * 1 j - + v setv 11 1 j for 11 1 i for 100 v valloc prog3"
ex17 = "x print 1 3 x * + x setq 2 x / x setq 2 x % 0 = if prog2 1 x != while 50 x setq x alloc prog3"
ex18 = "5 alloc"
ex19 = "x 3 + 5 defsub"
ex20 = "5 6 >="'''

'''e = Expression.from_program(ex17, d)
print(e)
res = e.evaluate({})
print(res)'''