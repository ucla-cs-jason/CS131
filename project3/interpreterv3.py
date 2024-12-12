from intbase import InterpreterBase, ErrorType
from brewparse import parse_program
import copy

class Value:
    def __init__(self, value=None, t=None):
        self.value = value
        self.vtype = t
    
    def __str__(self):
        return f'Value({self.value}, {self.vtype})'
    
    def __repr__(self):
        return self.__str__()


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.functions = dict()
        self.structs = dict()

    def get_var_exists(self, var_name, variables):
        if '.' in var_name:
            segments = var_name.split('.')
            curr_var = variables
            for seg in segments:
                if curr_var == None:
                    return 1
                elif type(curr_var) != dict:
                    return 2
                elif seg not in curr_var:
                    return 3
                else:
                    curr_var = curr_var[seg].value
            return 0
        else:
            return 1 if variables is None else 2 if type(variables) != dict else 3 if var_name not in variables else 0

    def get_var(self, var_name, variables):
        if self.get_var_exists(var_name, variables) != 0: return (False, None)
        if '.' in var_name:
            segments = var_name.split('.')
            curr_var = variables
            curr_val = None
            for seg in segments:
                if type(curr_var) == dict and seg in curr_var:
                    curr_val = curr_var[seg]
                    curr_var = curr_var[seg].value
                else:
                    return (False, None)
            return (True, curr_val)
        else:
            return (True, variables[var_name])
        
    def set_var(self, var_name, var_val, variables):
        if '.' in var_name:
            segments = var_name.split('.')
            curr_var = variables
            for i in range(len(segments)):
                seg = segments[i]
                if type(curr_var) == dict and seg in curr_var:
                    if i == len(segments) - 1:
                        curr_var[seg] = var_val
                    else:
                        curr_var = curr_var[seg].value
                else:
                    return False
            return True
        else:
            variables[var_name] = var_val
            return True
    
    def get_type_default(self, t):
        if t == 'bool':
            return False
        elif t == 'int':
            return 0
        elif t == 'string':
            return ''
        elif t == 'nil' or t in self.structs.keys():
            return None
        else:
            super().error(
                ErrorType.TYPE_ERROR,
                f'Cannot get type default for {t}',
            )
        
    def coerce(self, v, to_type):
        if v.vtype == None and v.value == None:
            return Value(self.get_type_default(to_type), to_type)
        elif v.vtype == to_type:
            return Value(v.value, v.vtype)
        elif v.vtype == 'int' and to_type == 'bool':
            return Value(False if v.value == 0 else True, 'bool')
        elif v.vtype == 'nil' and to_type in self.structs.keys():
            return Value(None, to_type)
        else:
            super().error(
                ErrorType.TYPE_ERROR,
                f'Coercion fails for {v.vtype} to {to_type}',
            )

    def eval_exp_var_val(self, evv, variables):
        # expression node
        # binary operation
        if evv.elem_type in ('+', '-', '*', '/','==', '<', '<=', '>', '>=', '!=', '||', '&&'):
            op1, op2 = evv.dict['op1'], evv.dict['op2']
            eval_op1, eval_op2 = self.eval_exp_var_val(op1, variables), self.eval_exp_var_val(op2, variables)
            # check for illegal usages
            # if evv.elem_type not in ('==', '!=', '||', '&&') and eval_op1.vtype != eval_op2.vtype:
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Incompatible types for operation: {eval_op1.vtype} {evv.elem_type} {eval_op2.vtype}',
            #     )
            # if (evv.elem_type in ('-', '*', '/') and eval_op1.vtype != 'int') or (evv.elem_type == '+' and eval_op1.vtype not in ('int', 'string')):
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Illegal arithmetic operation: {eval_op1.vtype} {evv.elem_type} {eval_op2.vtype}',
            #     )
            # if evv.elem_type in ('<', '>', '<=', '>=') and eval_op1.vtype != 'int':
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Illegal comparison operation: {eval_op1.vtype} {evv.elem_type} {eval_op2.vtype}',
            #     )
            # if evv.elem_type in ('||', '&&') and (eval_op1.vtype not in ('bool', 'int') or eval_op2.vtype not in ('bool', 'int')):
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Illegal logical operation: {eval_op1.vtype} {evv.elem_type} {eval_op2.vtype}',
            #     )
            # execute the binary operation
            def compare(eval_op1, eval_op2):
                if eval_op1.vtype in ('int', 'string', 'bool') or eval_op2.vtype in ('int', 'string', 'bool'):
                    if (eval_op1.vtype == 'int' and eval_op2.vtype == 'bool') or (eval_op2.vtype == 'int' and eval_op1.vtype == 'bool'):
                        eval_op1, eval_op2 = self.coerce(eval_op1, 'bool'), self.coerce(eval_op2, 'bool')
                    return eval_op1.value == eval_op2.value if eval_op1.vtype == eval_op2.vtype else False
                else:
                    if (eval_op1.vtype == 'nil' and eval_op2.value == None) or (eval_op2.vtype == 'nil' and eval_op1.value == None) or (eval_op1.vtype == 'nil' and eval_op2.value == 'nil'):
                        return True
                    elif (eval_op1.vtype == eval_op2.vtype) and (eval_op1.value == None) and (eval_op2.value == None):
                        return True
                    else:
                        return eval_op1.value == eval_op2.value if eval_op1.vtype == eval_op2.vtype else False
                    
            if evv.elem_type == '+':
                result = eval_op1.value + eval_op2.value
            elif evv.elem_type == '-':
                result = eval_op1.value - eval_op2.value
            elif evv.elem_type == '*':
                result = eval_op1.value * eval_op2.value
            elif evv.elem_type == '/':
                result = eval_op1.value // eval_op2.value
            elif evv.elem_type == '==':
                result = compare(eval_op1, eval_op2)
            elif evv.elem_type == '<':
                result = eval_op1.value < eval_op2.value
            elif evv.elem_type == '>':
                result = eval_op1.value > eval_op2.value
            elif evv.elem_type == '<=':
                result = eval_op1.value <= eval_op2.value
            elif evv.elem_type == '>=':
                result = eval_op1.value >= eval_op2.value
            elif evv.elem_type == '!=':
                result = not compare(eval_op1, eval_op2)
            elif evv.elem_type == '||':
                eval_op1, eval_op2 = self.coerce(eval_op1, 'bool'), self.coerce(eval_op2, 'bool')
                result = eval_op1.value or eval_op2.value
            elif evv.elem_type == '&&':
                eval_op1, eval_op2 = self.coerce(eval_op1, 'bool'), self.coerce(eval_op2, 'bool')
                result = eval_op1.value and eval_op2.value
            else:
                exit(1)
            return Value(result, eval_op1.vtype if evv.elem_type in ('+', '-', '*', '/') else 'bool')
        # unary operation
        elif evv.elem_type in ('neg', '!'):
            op1 = evv.dict['op1']
            eval_op1 = self.eval_exp_var_val(op1, variables)
            # check for illegal operations
            # if evv.elem_type == '!' and eval_op1.vtype not in ('bool', 'int'):
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Illegal logical operation: {eval_op1.vtype} {evv.elem_type} {eval_op1.vtype}',
            #     )
            # if evv.elem_type == 'neg' and eval_op1.vtype != 'int':
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Illegal logical operation: {eval_op1.vtype} {evv.elem_type} {eval_op1.vtype}',
            #     )
            result = -eval_op1.value if evv.elem_type == 'neg' else not self.coerce(eval_op1, 'bool').value
            return Value(result, 'int' if evv.elem_type == 'neg' else 'bool')
        # function call
        elif evv.elem_type == 'fcall':
            func_name, args = evv.dict['name'], evv.dict['args']
            eval_args = [self.eval_exp_var_val(arg, variables) for arg in args]
            result = self.eval_func_call(func_name, eval_args)
            # if result.vtype == 'void':
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Void function call cannot be evaluted',
            #     )
            return result
        # new command
        elif evv.elem_type == 'new':
            struct_name = evv.dict['var_type']
            # if struct_name not in self.structs:
            #     super().error(
            #         ErrorType.TYPE_ERROR,
            #         f'Unable to find struct: {struct_name}',
            #     )
            result = {field_name: Value(self.get_type_default(field_type), field_type) for field_name, field_type in self.structs[struct_name]}
            return Value(result, struct_name)
        # variable node
        elif evv.elem_type == 'var':
            var_name = evv.dict['name']
            var_found = self.get_var_exists(var_name, variables)
            if var_found == 0:
                var_found, var_val = self.get_var(var_name, variables)
                assert var_found
                return var_val
            else:
                if var_found == 1:
                    super().error(
                        ErrorType.FAULT_ERROR,
                        f'Variable {var_name} has not been defined - Variable node',
                    )
                else:
                    super().error(
                        ErrorType.NAME_ERROR,
                        f'Variable {var_name} has not been defined - Variable node',
                    )
        # value node
        elif evv.elem_type == 'int' or evv.elem_type == 'string' or evv.elem_type == 'bool':
            return Value(evv.dict['val'], evv.elem_type)
        elif evv.elem_type == 'nil':
            return Value(None, evv.elem_type)
    

    # returns a tuple (return value, is return triggered (if True then terminate all nested statements))
    # accepts outer_variables_list which is a list of dictionaries, where the first element is the most outer
    def execute_statements(self, statements, outer_variables_list):
        # variables that are declared within my scope
        inner_variables = dict()
        for statement in statements:
            # to execute an assignment statement
            def execute_assignment_statement(statement):
                var_name, expression = statement.dict['name'], statement.dict['expression']
                # check if variable exists
                found = False
                for d in [*outer_variables_list, inner_variables]:
                    # print(var_name, d)
                    check = self.get_var_exists(var_name, d)
                    if check == 0:
                        found = True
                    if check in (1, 2):
                        return check
                if not found:
                    return 3
                # assign to the variable declared in the most inner scope
                var_found, var = self.get_var(var_name, inner_variables)
                if var_found:
                    assert self.set_var(var_name,
                                        self.coerce(self.eval_exp_var_val(expression, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables}), var.vtype),
                                        inner_variables)
                else:
                    for i in range(len(outer_variables_list) - 1, -1, -1):
                        outer_variables = outer_variables_list[i]
                        var_found, var = self.get_var(var_name, outer_variables)
                        if var_found:
                            assert self.set_var(var_name,
                                                self.coerce(self.eval_exp_var_val(expression, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables}), var.vtype),
                                                outer_variables)
                return 0

            # variable definition statement
            if statement.elem_type == 'vardef':
                var_name, var_type = statement.dict['name'], statement.dict['var_type']
                if self.get_var_exists(var_name, inner_variables) != 3:
                    super().error(
                        ErrorType.NAME_ERROR,
                        f'Variable {var_name} defined more than once',
                    )
                assert self.set_var(var_name, Value(self.get_type_default(var_type), var_type), inner_variables)
            # assignment statement
            elif statement.elem_type == '=':
                var_name = statement.dict['name']
                exec_result = execute_assignment_statement(statement)
                if exec_result == 1:
                    super().error(
                        ErrorType.FAULT_ERROR,
                        f'Variable {var_name} has not been defined - Assignment',
                    )
                elif exec_result in (2, 3):
                    super().error(
                        ErrorType.NAME_ERROR,
                        f'Variable {var_name} has not been defined - Assignment',
                    )
            # function call statement
            elif statement.elem_type == 'fcall':
                func_name, args = statement.dict['name'], statement.dict['args']
                eval_args = [self.eval_exp_var_val(arg, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables}) for arg in args]
                self.eval_func_call(func_name, eval_args)
            # if statement
            elif statement.elem_type == 'if':
                condition, then_statements, else_statements = statement.dict['condition'], statement.dict['statements'], statement.dict['else_statements']
                eval_condition = self.eval_exp_var_val(condition, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables})
                # check if conditions evaluates to a boolean
                # if eval_condition.vtype != 'bool' and eval_condition.vtype != 'int':
                #     super().error(
                #         ErrorType.TYPE_ERROR,
                #         f'Condition {eval_condition.vtype} is not a boolean or integer',
                #     )
                # execute then statement or else statement
                if eval_condition.value:
                    result, is_returned = self.execute_statements(then_statements, [*outer_variables_list, inner_variables])
                    if is_returned:
                        return (result, is_returned)
                elif else_statements:
                    result, is_returned = self.execute_statements(else_statements, [*outer_variables_list, inner_variables])
                    if is_returned:
                        return (result, is_returned)
            # for loop statement
            elif statement.elem_type == 'for':
                init, condition, update, loop_statements = statement.dict['init'], statement.dict['condition'], statement.dict['update'], statement.dict['statements']
                # execute the initialization statement
                if execute_assignment_statement(init) != 0:
                    var_name = init.dict['name']
                    super().error(
                        ErrorType.NAME_ERROR,
                        f'Variable {var_name} has not been defined - For init',
                    )
                while True:
                    eval_condition = self.eval_exp_var_val(condition, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables})
                    # check if conditions evaluates to a boolean
                    # if eval_condition.vtype != 'bool' and eval_condition.vtype != 'int':
                    #     super().error(
                    #         ErrorType.TYPE_ERROR,
                    #         f'Condition {eval_condition.vtype} is not a boolean or integer',
                    #     )
                    # break loop if condition evaluates to false
                    if not eval_condition.value:
                        break
                    # execute loop statements
                    result, is_returned = self.execute_statements(loop_statements, [*outer_variables_list, inner_variables])
                    if is_returned:
                        return (result, is_returned)
                    # execute update statement
                    if execute_assignment_statement(update) != 0:
                        var_name = update.dict['name']
                        super().error(
                            ErrorType.NAME_ERROR,
                            f'Variable {var_name} has not been defined - For update',
                        )
            # return statement
            elif statement.elem_type == 'return':
                expression = statement.dict['expression']
                if expression:
                    return self.eval_exp_var_val(expression, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables}), True
                else:
                    return Value(None, None), False
                
        return Value(None, None), False
    
    def eval_func_call(self, func, args):
        # predefined functions
        result = None
        # print function
        if func == 'print':
            super().output(''.join(['nil' if arg.value is None else str(arg.value).lower() if arg.vtype == 'bool' else str(arg.value) for arg in args]))
            return Value(None, 'void')
        # inputi function
        elif func == 'inputi':
            if len(args) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'No inputi() function found that takes > 1 parameter',
                )
            if args:
                super().output(args[0].value)
            result = super().get_input()
            result = int(result)
            return Value(result, 'int')
        # inputs function
        elif func == 'inputs':
            if len(args) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'No inputs() function found that takes > 1 parameter',
                )
            if args:
                super().output(args[0].value)
            result = super().get_input()
            return Value(result, 'string')
        # our own functions
        else:
            # check if function exists
            if (func, len(args)) not in self.functions:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'Function {(func, len(args))} has not been defined',
                )
            else:
                func = self.functions[(func, len(args))]

            # set up variables from args
            variables = dict()
            statements, arg_nodes = func.dict['statements'], func.dict['args']
            for i in range(len(args)):
                variables[arg_nodes[i].dict['name']] = self.coerce(args[i], arg_nodes[i].dict['var_type'])

            # execute the statements and return result
            result, _ = self.execute_statements(statements, [variables])
            if func.dict['return_type'] != 'void':
                result = self.coerce(result, func.dict['return_type'])
            else:
                result = Value(None, 'void')
            return result

    def run(self, program):
        parsed_program = parse_program(program)

        for struct in parsed_program.dict['structs']:
            name, fields = struct.dict['name'], struct.dict['fields']
            self.structs[name] = [(f.dict['name'], f.dict['var_type']) for f in fields]
            for f in fields:
                field_type = f.dict['var_type']
                if field_type not in ['int', 'string', 'bool', *self.structs.keys()]:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'Struct {field_type} not recogniezd',
                    )

        for func in parsed_program.dict['functions']:
            name, num_args, args, return_type = func.dict['name'], len(func.dict['args']), func.dict['args'], func.dict['return_type']
            self.functions[(name, num_args)] = func
            if return_type not in ['int', 'string', 'bool', 'void', *self.structs.keys()]:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'Function return type {return_type} not recogniezd',
                )
            for arg in args:
                arg_type = arg.dict['var_type']
                if arg_type not in ['int', 'string', 'bool', *self.structs.keys()]:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'Function argument type {arg_type} not recogniezd',
                    )

        if ('main', 0) not in self.functions:
            super().error(
                ErrorType.NAME_ERROR,
                'No main() function was found',
            )

        # self.static_type_checking()

        self.eval_func_call('main', [])

    '''
    Use of an invalid/undefined/missing type for a parameter or return type must result in an error of ErrorType.TYPE_ERROR.
    This check should happen before the execution of the main function, and the error should be reported
    no matter if the function in question is used in execution or not.
    '''
    def check_same_type_or_coerce(self, type1, type2):
        return (type1 == 'bool' and type2 == 'int') or (type1 == type2) or (type1 in self.structs.keys() and type2 == 'nil')
    
    def check_function_call(self, func_name, args, variables):
        for i in range(len(args)):
            provided_arg_type = self.get_type_evv(args[i], variables)
            if provided_arg_type == 'void':
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Void arguments cannot be used for function calls',
                )

        if func_name == 'print':
            return 'void'
        elif func_name == 'inputi':
            return 'int'
        elif func_name == 'inputs':
            return 'string'
        else:
            if (func_name, len(args)) not in self.functions:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'ST Check: Function not found',
                )
            func = self.functions[(func_name, len(args))]
            for i in range(len(args)):
                func_arg_type, provided_arg_type = func.dict['args'][i].dict['var_type'], self.get_type_evv(args[i], variables)
                if not self.check_same_type_or_coerce(func_arg_type, provided_arg_type):
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'ST Check: Function argument {func_arg_type} is given a {provided_arg_type}',
                    )
            return func.dict['return_type']
        
    def get_var_type(self, var_name, variables):
        if '.' in var_name:
            segments = var_name.split('.')
            if segments[0] not in variables:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Cannot find type of variable - 1: {var_name}',
                )
            else:
                curr_type = variables[segments[0]]
                if curr_type not in self.structs:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'ST Check: Cannot find type of variable - 2: {var_name}',
                    )
                for i in range(1, len(segments)):
                    found = None
                    if curr_type not in self.structs:
                        super().error(
                            ErrorType.TYPE_ERROR,
                            f'ST Check: Cannot find type of variable - 3: {var_name}',
                        )
                    for field_name, field_type in self.structs[curr_type]:
                        if field_name == segments[i]:
                            curr_type = field_type
                            found = True
                            break
                    if not found:
                        super().error(
                            ErrorType.NAME_ERROR,
                            f'ST Check: Cannot find type of variable - 4: {var_name}',
                        )
                return curr_type
        else:
            if var_name not in variables:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'ST Check: Cannot find type of variable - 5: {var_name}',
                )
            return variables[var_name]

    def get_type_evv(self, evv, variables):
        if evv.elem_type in ('+', '-', '*', '/','==', '<', '<=', '>', '>=', '!=', '||', '&&'):
            op1, op2 = evv.dict['op1'], evv.dict['op2']
            eval_op1, eval_op2 = self.get_type_evv(op1, variables), self.get_type_evv(op2, variables)
            if evv.elem_type == '+' and not ((eval_op1 == 'int' and eval_op2 == 'int') or (eval_op1 == 'string' and eval_op2 == 'string')):
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Type {eval_op1} cannot perform binary operation {evv.elem_type} with {eval_op2}',
                )
            elif (evv.elem_type in ('-', '*', '/') and (eval_op1 != 'int' or eval_op2 != 'int')):
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Type {eval_op1} cannot perform binary operation {evv.elem_type} with {eval_op2}',
                )
            elif evv.elem_type in ('<', '>', '<=', '>=') and (eval_op1 != 'int' or eval_op2 != 'int'):
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Type {eval_op1} cannot perform binary operation {evv.elem_type} with {eval_op2}',
                )
            elif evv.elem_type in ('||', '&&') and (eval_op1 not in ('bool', 'int') or eval_op2 not in ('bool', 'int')):
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Type {eval_op1} cannot perform binary operation {evv.elem_type} with {eval_op2}',
                )
            elif evv.elem_type in ('==', '!=') and not ((eval_op1 == 'int' and eval_op2 == 'bool') or (eval_op1 == 'bool' and eval_op2 == 'int') or (eval_op1 == eval_op2) or (eval_op1 in self.structs.keys() and eval_op2 == 'nil') or (eval_op1 == 'nil' and eval_op2 in self.structs.keys())):
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Type {eval_op1} cannot perform binary operation {evv.elem_type} with {eval_op2}',
                )
            return eval_op1 if evv.elem_type in ('+', '-', '*', '/') else 'bool'
        elif evv.elem_type in ('neg', '!'):
            op1 = evv.dict['op1']
            eval_op1 = self.get_type_evv(op1, variables)
            if (evv.elem_type == 'neg' and eval_op1 == 'int') or (evv.elem_type == '!' and eval_op1 == 'bool') or (evv.elem_type == '!' and eval_op1 == 'int'):
                return 'int' if evv.elem_type == 'neg' else 'bool'
            else:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Cannot perform unary operation {evv.elem_type} on {eval_op1}',
                )
        elif evv.elem_type == 'fcall':
            func_name, args = evv.dict['name'], evv.dict['args']
            func_return_type = self.check_function_call(func_name, args, variables)
            if func_return_type == 'void':
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Cannot evaluate void function call as an expression',
                )
            return func_return_type
        elif evv.elem_type == 'new':
            var_type = evv.dict['var_type']
            if var_type not in self.structs.keys():
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'ST Check: Cannot new type {var_type}',
                )
            return var_type
        elif evv.elem_type == 'var':
            var_name = evv.dict['name']
            var_type = self.get_var_type(var_name, variables)
            return var_type
        elif evv.elem_type == 'int' or evv.elem_type == 'string' or evv.elem_type == 'bool':
            return evv.elem_type
        elif evv.elem_type == 'nil':
            return evv.elem_type

    def check_statements(self, statements, variables, return_type):
        variables = copy.deepcopy(variables)

        for statement in statements:
            if statement.elem_type == 'vardef':
                name, var_type = statement.dict['name'], statement.dict['var_type']
                if var_type not in ['int', 'string', 'bool', *self.structs.keys()]:
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'ST Check: Unrecognized type: {var_type}',
                    )
                else: variables[name] = var_type
            elif statement.elem_type == '=':
                name, expression = statement.dict['name'], statement.dict['expression']
                var_type = self.get_var_type(name, variables)
                if name in variables and not self.check_same_type_or_coerce(var_type, self.get_type_evv(expression, variables)):
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'ST Check: Expression cannot be assigned to {name}: {var_type} = {self.get_type_evv(expression, variables)}',
                    )
            elif statement.elem_type == 'fcall':
                func_name, args = statement.dict['name'], statement.dict['args']
                self.check_function_call(func_name, args, variables)
            elif statement.elem_type == 'if':
                condition, then_statements, else_statements = statement.dict['condition'], statement.dict['statements'], statement.dict['else_statements']
                if not self.check_same_type_or_coerce('bool', self.get_type_evv(condition, variables)):
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'ST Check: If condition type evaluates to {self.get_type_evv(condition, variables)}',
                    )
                self.check_statements(then_statements, variables, return_type)
                if else_statements: self.check_statements(else_statements, variables, return_type)
            elif statement.elem_type == 'for':
                init, condition, update, loop_statements = statement.dict['init'], statement.dict['condition'], statement.dict['update'], statement.dict['statements']
                self.check_statements([init], variables, return_type)
                if not self.check_same_type_or_coerce('bool', self.get_type_evv(condition, variables)):
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'ST Check: If condition type evaluates to {self.get_type_evv(condition, variables)}',
                    )
                self.check_statements([update], variables, return_type)
                self.check_statements(loop_statements, variables, return_type)
            elif statement.elem_type == 'return':
                expression = statement.dict['expression']
                if expression and return_type == 'void':
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'ST Check: Void return type should not have an expression',
                    )
                if expression:
                    expression_type = self.get_type_evv(expression, variables)
                    if not self.check_same_type_or_coerce(return_type, expression_type):
                        # void TODO
                        super().error(
                            ErrorType.TYPE_ERROR,
                            f'ST Check: Return type {return_type} does not match {expression_type}',
                        )

    def static_type_checking(self):
        for func in self.functions.values():
            statements, return_type, args = func.dict['statements'], func.dict['return_type'], func.dict['args']
            variables = dict()
            for arg in args:
                arg_name, arg_type = arg.dict['name'], arg.dict['var_type']
                variables[arg_name] = arg_type
            self.check_statements(statements, variables, return_type)
            
