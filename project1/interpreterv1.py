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
        if evv.elem_type == '+' or evv.elem_type == '-':
            op1, op2 = evv.dict['op1'], evv.dict['op2']
            eval_op1, eval_op2 = self.eval_exp_var_val(op1, variables), self.eval_exp_var_val(op2, variables)
            if type(eval_op1) != type(eval_op2):
                super().error(
                    ErrorType.TYPE_ERROR,
                    'Incompatible types for arithmetic operation',
                )
            result = eval_op1 + eval_op2 if evv.elem_type == '+' else eval_op1 - eval_op2
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
            return variables[var_name]
        # value node
        elif evv.elem_type == 'int' or evv.elem_type == 'string':
            result = evv.dict['val']
        
        self.debug('EVV evaluated to be:', result)
        return result
    
    def eval_func_call(self, func, args):
        # predefined functions
        result = None
        if func == 'print':
            super().output(''.join([str(arg) for arg in args]))
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
        # our own functions
        else:
            if func not in self.functions:
                super().error(
                    ErrorType.NAME_ERROR,
                    f'Function {func} has not been defined',
                )
            else:
                func = self.functions[func]

            variables = dict()
            self.debug('Func dict =', func.dict)

            statements = func.dict['statements']
            for statement in statements:
                self.debug('Statement type =', statement.elem_type)
                self.debug('Statement dict =', statement.dict)
                # variable definition statement
                if statement.elem_type == 'vardef':
                    var_name = statement.dict['name']
                    if var_name in variables:
                        super().error(
                            ErrorType.NAME_ERROR,
                            f'Variable {var_name} defined more than once',
                        )
                    variables[var_name] = None
                # assignment statement
                elif statement.elem_type == '=':
                    var_name, expression = statement.dict['name'], statement.dict['expression']
                    if var_name not in variables:
                        super().error(
                            ErrorType.NAME_ERROR,
                            f'Variable {var_name} has not been defined',
                        )
                    variables[var_name] = self.eval_exp_var_val(expression, variables)
                # function call statement
                else:
                    func_name, args = statement.dict['name'], statement.dict['args']
                    eval_args = [self.eval_exp_var_val(arg, variables) for arg in args]
                    self.eval_func_call(func_name, eval_args)
        return result

    def run(self, program):
        parsed_program = parse_program(program)
        self.debug('Program dict =', parsed_program.dict)

        for func in parsed_program.dict['functions']:
            name = func.dict['name']
            self.functions[name] = func

        if 'main' not in self.functions:
            super().error(
                ErrorType.NAME_ERROR,
                'No main() function was found',
            )

        main_func = self.functions['main']
        self.debug('Main Func dict =', main_func.dict)
        self.eval_func_call('main', [])
