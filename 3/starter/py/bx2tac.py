import argparse, sys, json
import bx_parser as lexer_parser
import bx_ast_classes as ast
from py.tac2asm import compile_tac
from typing import List

# ------------------------------------------------------------------------------#
# tac file delivery
# ------------------------------------------------------------------------------#

class Code_as_tac_json:
    """ This class creates the tac file in json format
        that implements the given method bmm or tmm """
    
    def __init__(self, ast_classes: ast.AstCode, method: str) -> None:
        self.ast_code = Code(ast_classes.statements, method)
        self.method = method
    
    def json_tac(self) -> List:
        return [{"proc": "@main",
                "body": [statement.json_field for statement in self.ast_code.instructions] }]

# ------------------------------------------------------------------------------#
# ast to tac code conversion Munch Methods
# ------------------------------------------------------------------------------#

# maps for converting operations
binopcode_dict = { 
    "addition": "add", "subtraction": "sub", 
    "multiplication": "mul", "division": "div", 
    "modulus": "mod", "bitwise-and": "and", 
    "logical-shift-right": "shr", "bitwise-or": "or", 
    "logical-shift-left": "shl", "bitwise-xor": "xor"
}

uniopcode_dict = {
    "opposite": "neg", "bitwise-negation": "not"
}

class Code:
    def __init__(self, statements: List, method: str) -> None:
        self.method: str = method
        self.statements: List = statements
        self.temp_var_map: dict = {}
        self.global_reg_counter: int = 0
        self.instructions: List = []
        self.init_parse()

    def fresh_temp(self, name: str = '') -> str:
        """ Creates and returns a fresh temporary """
        fresh_temp = f"%{self.global_reg_counter}"
        self.global_reg_counter += 1
        # if the temp has a variable name then append it to temp_map
        if name != '':
            self.temp_var_map[name] = fresh_temp
        return fresh_temp

    def return_temp(self, name: str) -> str:
        """ Returns the temp allocator """
        if name in self.temp_var_map:
            temp = self.temp_var_map[name]
        else:
            temp = self.fresh_temp(name)
        return temp

    def init_parse(self) -> None:
        """ Converts all statements to singluar json objects 
            and stores them in the instructions variable """

        for elem in self.statements:   # loop through all statements in the body
            if self.method == "bmm":   # Otherwise treat the statement as bmm
                self.bmm_statement(elem)
            elif self.method == "tmm":   # Otherwise treat the statement as tmm
                self.tmm_statement(elem)
            else:
                print("This is not supposed to happen. Apocalypse!")
                sys.exit(1)

    # ---------------------------------------------------------------------#
    # tmm method
    # ---------------------------------------------------------------------#

    def tmm_expression(self, expression: ast.Expression, final_result: str) -> None:
        """ ast.Evaluates the expression and adds it to instructions list as json object """

        if isinstance(expression, ast.ExpressionVar):
            stored_temp = self.return_temp(expression.name)
            self.instructions.append(ast.Tac_statement('copy', 
                                                    [stored_temp], 
                                                    final_result))
        elif isinstance(expression, ast.ExpressionInt):
            val = expression.value
            self.instructions.append(ast.Tac_statement('const',
                                                    [val],
                                                    final_result))
        elif isinstance(expression, ast.ExpressionUniOp):
            result_temp = self.fresh_temp()
            self.tmm_expression(expression.argument, result_temp)
            self.instructions.append(ast.Tac_statement(uniopcode_dict[expression.operator],
                                                   [result_temp], 
                                                   final_result))
        elif isinstance(expression, ast.ExpressionBinOp):
            result_temp_left = self.fresh_temp()
            result_temp_right = self.fresh_temp()
            self.tmm_expression(expression.left_arg, result_temp_left)
            self.tmm_expression(expression.right_arg, result_temp_right)
            self.instructions.append(ast.Tac_statement(binopcode_dict[expression.operator], 
                                                   [result_temp_left, result_temp_right], 
                                                   final_result))
        else:   # Should be unreachable
            raise ValueError(f'Unrecognized <expression>: {expression}')

    def tmm_statement(self, statement: ast.Statement) -> None :
        """ Appends instructions as singluar json objects using the tmm method """
        
        if isinstance(statement, ast.Vardecl):
            temp_reg = self.fresh_temp(statement.name.name)
            init = statement.init
            self.tmm_expression(init, 
                                temp_reg)
        elif isinstance(statement, ast.Assign):
            result_temp = self.return_temp(statement.left)
            right = statement.right
            self.tmm_expression(right,
                                result_temp)
        elif isinstance(statement, ast.Eval):
            result_temp = self.fresh_temp()
            eval_arg = statement.eval_argument
            self.tmm_expression(eval_arg, result_temp)
            self.instructions.append(ast.Tac_statement("print", 
                                                    [result_temp], 
                                                    None))
        else:   # Should be unreachable
            raise ValueError(f'Unrecognized <statement>: {statement}')

    # ---------------------------------------------------------------------#
    # bmm method
    # ---------------------------------------------------------------------#

    def bmm_expression(self, expression: ast.Expression) -> str:
        """ ast.Evaluates the expression and adds it to instructions list as json object """
        
        if isinstance(expression, ast.ExpressionVar):
            return self.return_temp(expression.name)
        
        elif isinstance(expression, ast.ExpressionInt):
            result_temp = self.fresh_temp()
            self.instructions.append(ast.Tac_statement('const', 
                                                    [expression.value], 
                                                    result_temp))
            return result_temp
        elif isinstance(expression, ast.ExpressionUniOp):
            result_temp = self.fresh_temp()
            val_temp  = self.bmm_expression(expression.argument)
            self.instructions.append(ast.Tac_statement(uniopcode_dict[expression.operator], 
                                                   [val_temp],
                                                   result_temp))
            return result_temp
        elif isinstance(expression, ast.ExpressionBinOp):
            left_arg = expression.left_arg
            right_arg = expression.right_arg
            arguments = [self.bmm_expression(left_arg), 
                         self.bmm_expression(right_arg)]
            result_temp = self.fresh_temp()
            self.instructions.append(ast.Tac_statement(binopcode_dict[expression.operator], 
                                                   arguments, 
                                                   result_temp))
            return result_temp
        else:   # Should be unreachable
            raise ValueError(f'Unrecognized <expression>: {expression}')

    def bmm_statement(self, statement: ast.Statement) -> None:
        """ Appends instructions as singluar json objects using the bmm method """
        
        if isinstance(statement, ast.Vardecl):
            result_temp = self.fresh_temp(statement.name.name)
            val_temp = self.bmm_expression(statement.init)
            self.instructions.append(ast.Tac_statement("copy", 
                                                    [val_temp],
                                                    result_temp))
        elif isinstance(statement, ast.Assign):
            result_temp = self.return_temp(statement.left)
            val_temp = self.bmm_expression(statement.right)
            self.instructions.append(ast.Tac_statement("copy", 
                                                    [val_temp], 
                                                    result_temp))
        elif isinstance(statement, ast.Eval):
            result_temp = self.bmm_expression(statement.eval_argument)
            self.instructions.append(ast.Tac_statement("print", 
                                                    [result_temp], 
                                                    None))
        else:   # Should be unreachable
            raise ValueError(f'Unrecognized <statement>: {statement}')


# ------------------------------------------------------------------------------#
# Main function
# ------------------------------------------------------------------------------#

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Get method for conversion and filetype.')
    parser.add_argument('--tmm', dest='tmm', action="store_true", default=False)
    parser.add_argument('--bmm', dest='bmm', action='store_true', default=False)
    parser.add_argument('filename', metavar="FILE", type=str, nargs=1)
    args = parser.parse_args(sys.argv[1:])
    
    method = "bmm"                  # select default method for conversion as bmm
    if args.tmm:                    # change method to tmm
        method = "tmm"
    filename = args.filename[0]     # get the filename

    with open(filename, 'r') as fp:             # read the bx code as text
        code = fp.read()

    ast_ = lexer_parser.run_parser(code)        # run lexer and parser
    if ast_ is None: 
        raise SyntaxError("at line 1")          # exit if error occured while parsing 
    ast_.check_syntax()                         # check syntax
    print('reached tac json')
    tac_code = Code_as_tac_json(ast_, method)   # convert ast code to json
    print("tac json created")
    tac_filename = filename[:-2] + 'tac.json'   # get new file name
    with open(tac_filename, 'w') as fp:         # save the file
        json.dump(tac_code.json_tac(), fp, indent=4)

    compile_tac(tac_filename)
