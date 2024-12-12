from intbase import InterpreterBase, ErrorType
from brewparse import parse_program


class Interpreter(InterpreterBase):
    def __init__(self, console_output=True, inp=None, trace_output=False):
        super().__init__(console_output, inp)
        self.functions = dict()
        self.trace_output = False # trace_output
        self.debug('\n')

    def debug(self, *messages):
        if self.trace_output:
            print('[DEBUG] ' + ' '.join(str(message) for message in messages))


    def eval_exp_var_val(self, evv, variables):
        self.debug('EVV type =', evv.elem_type)
        self.debug('EVV dict =', evv.dict)

        # expression node
        # binary operation
        if evv.elem_type in ('+', '-', '*', '/','==', '<', '<=', '>', '>=', '!=', '||', '&&'):
            op1, op2 = evv.dict['op1'], evv.dict['op2']
            eval_op1, eval_op2 = self.eval_exp_var_val(op1, variables), self.eval_exp_var_val(op2, variables)
            # check for illegal usages
            if evv.elem_type not in ('==', '!=') and type(eval_op1) != type(eval_op2):
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'Incompatible types for operation: {type(eval_op1)} {evv.elem_type} {type(eval_op2)}',
                )
            if (evv.elem_type in ('-', '*', '/') and type(eval_op1) != int) or (evv.elem_type == '+' and type(eval_op1) not in (int, str)):
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'Illegal arithmetic operation: {type(eval_op1)} {evv.elem_type} {type(eval_op2)}',
                )
            if evv.elem_type in ('<', '>', '<=', '>=') and type(eval_op1) is not int:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'Illegal comparison operation: {type(eval_op1)} {evv.elem_type} {type(eval_op2)}',
                )
            if evv.elem_type in ('||', '&&') and type(eval_op1) is not bool:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'Illegal logical operation: {type(eval_op1)} {evv.elem_type} {type(eval_op2)}',
                )
            # execute the binary operation
            if evv.elem_type == '+':
                result = eval_op1 + eval_op2
            elif evv.elem_type == '-':
                result = eval_op1 - eval_op2
            elif evv.elem_type == '*':
                result = eval_op1 * eval_op2
            elif evv.elem_type == '/':
                result = eval_op1 // eval_op2
            elif evv.elem_type == '==':
                result = eval_op1 == eval_op2 if type(eval_op1) == type(eval_op2) else False
            elif evv.elem_type == '<':
                result = eval_op1 < eval_op2
            elif evv.elem_type == '>':
                result = eval_op1 > eval_op2
            elif evv.elem_type == '<=':
                result = eval_op1 <= eval_op2
            elif evv.elem_type == '>=':
                result = eval_op1 >= eval_op2
            elif evv.elem_type == '!=':
                result = eval_op1 != eval_op2 if type(eval_op1) == type(eval_op2) else True
            elif evv.elem_type == '||':
                result = eval_op1 or eval_op2
            elif evv.elem_type == '&&':
                result = eval_op1 and eval_op2
        # unary operation
        elif evv.elem_type in ('neg', '!'):
            op1 = evv.dict['op1']
            eval_op1 = self.eval_exp_var_val(op1, variables)
            # check for illegal operations
            if evv.elem_type == '!' and type(eval_op1) is not bool:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'Illegal logical operation: {type(eval_op1)} {evv.elem_type} {type(eval_op1)}',
                )
            if evv.elem_type == 'neg' and type(eval_op1) is not int:
                super().error(
                    ErrorType.TYPE_ERROR,
                    f'Illegal logical operation: {type(eval_op1)} {evv.elem_type} {type(eval_op1)}',
                )
            result = -eval_op1 if evv.elem_type == 'neg' else not eval_op1
        # function call
        elif evv.elem_type == 'fcall':
            func_name, args = evv.dict['name'], evv.dict['args']
            eval_args = [self.eval_exp_var_val(arg, variables) for arg in args]
            result = self.eval_func_call(func_name, eval_args)
        # variable node
        elif evv.elem_type == 'var':
            var_name = evv.dict['name']
            if var_name not in variables:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'Variable {var_name} has not been defined',
                )
            result = variables[var_name]
        # value node
        elif evv.elem_type == 'int' or evv.elem_type == 'string' or evv.elem_type == 'bool':
            result = evv.dict['val']
        elif evv.elem_type == 'nil':
            result = None
        
        self.debug('EVV evaluated to be:', result)
        return result
    
    
    def eval_func_call(self, func, args):
        # predefined functions
        result = None
        # print function
        if func == 'print':
            super().output(''.join(['nil' if arg is None else str(arg).lower() if isinstance(arg, bool) else str(arg) for arg in args]))
        # inputi function
        elif func == 'inputi':
            if len(args) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'No inputi() function found that takes > 1 parameter',
                )
            if args:
                super().output(args[0])
            result = super().get_input()
            result = int(result)
        # inputs function
        elif func == 'inputs':
            if len(args) > 1:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'No inputs() function found that takes > 1 parameter',
                )
            if args:
                super().output(args[0])
            result = super().get_input()
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

            self.debug('Func dict =', func.dict)
            # set up variables from args
            variables = dict()
            statements, arg_nodes = func.dict['statements'], func.dict['args']
            for i in range(len(args)):
                variables[arg_nodes[i].dict['name']] = args[i]

            # execute the statements and return result
            result, _ = self.execute_statements(statements, [variables])
            
        return result
    
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
                if all(var_name not in d for d in [*outer_variables_list, inner_variables]):
                    return False
                # assign to the variable declared in the most inner scope
                if var_name in inner_variables:
                    inner_variables[var_name] = self.eval_exp_var_val(expression, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables})
                else:
                    for i in range(len(outer_variables_list) - 1, -1, -1):
                        outer_variables = outer_variables_list[i]
                        if var_name in outer_variables:
                            outer_variables[var_name] = self.eval_exp_var_val(expression, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables})
                return True

            self.debug('Statement type =', statement.elem_type)
            self.debug('Statement dict =', statement.dict)
            # variable definition statement
            if statement.elem_type == 'vardef':
                var_name = statement.dict['name']
                if var_name in inner_variables:
                    super().error(
                        ErrorType.NAME_ERROR,
                        f'Variable {var_name} defined more than once',
                    )
                inner_variables[var_name] = None
            # assignment statement
            elif statement.elem_type == '=':
                if not execute_assignment_statement(statement):
                    var_name = statement.dict['name']
                    super().error(
                        ErrorType.NAME_ERROR,
                        f'Variable {var_name} has not been defined',
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
                if not isinstance(eval_condition, bool):
                    super().error(
                        ErrorType.TYPE_ERROR,
                        f'Condition {type(eval_condition)} is not a boolean',
                    )
                # execute then statement or else statement
                if eval_condition:
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
                if not execute_assignment_statement(init):
                    var_name = init.dict['name']
                    super().error(
                        ErrorType.NAME_ERROR,
                        f'Variable {var_name} has not been defined',
                    )
                while True:
                    eval_condition = self.eval_exp_var_val(condition, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables})
                    # check if conditions evaluates to a boolean
                    if not isinstance(eval_condition, bool):
                        super().error(
                            ErrorType.TYPE_ERROR,
                            f'Condition {type(eval_condition)} is not a boolean',
                        )
                    # break loop if condition evaluates to false
                    if not eval_condition:
                        break
                    # execute loop statements
                    result, is_returned = self.execute_statements(loop_statements, [*outer_variables_list, inner_variables])
                    if is_returned:
                        return (result, is_returned)
                    # execute update statement
                    if not execute_assignment_statement(update):
                        var_name = update.dict['name']
                        super().error(
                            ErrorType.NAME_ERROR,
                            f'Variable {var_name} has not been defined',
                        )
            # return statement
            elif statement.elem_type == 'return':
                expression = statement.dict['expression']
                return (self.eval_exp_var_val(expression, {**{k: v for d in outer_variables_list for k, v in d.items()}, **inner_variables}), True) if expression else (None, True)
        return (None, False)

    def run(self, program):
        parsed_program = parse_program(program)
        self.debug('Program dict =', parsed_program.dict)

        for func in parsed_program.dict['functions']:
            name, num_args = func.dict['name'], len(func.dict['args'])
            self.functions[(name, num_args)] = func

        if ('main', 0) not in self.functions:
            super().error(
                ErrorType.NAME_ERROR,
                'No main() function was found',
            )

        self.debug('Main Func dict =', self.functions[('main', 0)].dict)
        self.eval_func_call('main', [])
