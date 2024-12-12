from intbase import InterpreterBase


class LazyExpression:
    def __init__(self, f):
        self.f = f
        self.evaled = False
        self.eval_result = None

    def execute(self):
        if not self.evaled:
            result = self.f()
            self.evaled = True
            self.eval_result = result
        return self.eval_result
    
    def __repr__(self):
        return f"LazyExpression(f={self.f}, evaled={self.evaled}, eval_result={self.eval_result})"
    

class ExecutionResult:
    def __init__(self, is_success, arg):
        self.is_success = is_success
        self.arg = arg

    def get_error(self):
        return self.arg
    
    def get_error_type(self):
        return self.arg[0]
    
    def get_value(self):
        return self.arg


# Enumerated type for our different language data types
class Type:
    INT = "int"
    BOOL = "bool"
    STRING = "string"
    NIL = "nil"


# Represents a value, which has a type and its value
class Value:
    def __init__(self, type, value=None):
        self.t = type
        self.v = value

    def value(self):
        return self.v

    def type(self):
        return self.t
    
    def __repr__(self):
        return f"Value(type={self.t}, value={self.v})"
    
    def __eq__(self, other):
        if isinstance(other, Value):
            return self.t == other.t and self.v == other.v
        return False


def create_value(val):
    if val == InterpreterBase.TRUE_DEF:
        return Value(Type.BOOL, True)
    elif val == InterpreterBase.FALSE_DEF:
        return Value(Type.BOOL, False)
    elif val == InterpreterBase.NIL_DEF:
        return Value(Type.NIL, None)
    elif isinstance(val, str):
        return Value(Type.STRING, val)
    elif isinstance(val, int):
        return Value(Type.INT, val)
    else:
        raise ValueError("Unknown value type")


def get_printable(val):
    if val.type() == Type.INT:
        return str(val.value())
    if val.type() == Type.STRING:
        return val.value()
    if val.type() == Type.BOOL:
        if val.value() is True:
            return "true"
        return "false"
    return None