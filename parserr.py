class SyntaxError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def error(self, msg="Syntax error"):
        raise SyntaxError(f"{msg} at token {self.current_token}")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def check_type(self, token_type):
        return self.current_token and self.current_token[0] == token_type

    def check_value(self, value):
        return self.current_token and self.current_token[1] == value

    def eat(self, token_type=None, token_value=None):
        if token_type and not self.check_type(token_type):
            self.error(f"Expected token type {token_type}")
        if token_value and not self.check_value(token_value):
            self.error(f"Expected token value {token_value}")
        self.advance()

    def parse_program(self):
        # program <ID> ; <block> .
        self.eat("KEYWORD", "program")
        prog_name = self.parse_identifier()
        self.eat("DELIMITER", ";")
        block = self.parse_block()
        self.eat("DELIMITER", ".")
        return ("Program", prog_name, block)

    def parse_block(self):
        # <var_section> <compound_statement>
        var_section = self.parse_var_section()
        compound = self.parse_compound_statement()
        return ("Block", var_section, compound)

    def parse_var_section(self):
        # var <var_declaration_list> ; | epsilon
        if self.check_type("KEYWORD") and self.check_value("var"):
            self.eat("KEYWORD", "var")
            decls = self.parse_var_declaration_list()
            self.eat("DELIMITER", ";")
            return ("VarSection", decls)
        # "Костыль" — игнорируем ключевое слово var и переходим дальше
        else:
            return ("VarSection", [])

    def parse_var_declaration_list(self):
        declarations = []
        declarations.append(self.parse_var_declaration())
        while self.check_type("DELIMITER") and self.current_token[1] == ";":
            self.eat("DELIMITER", ";")
            if self.check_type("ID"):  # Мы можем обработать идентификаторы переменных
                declarations.append(self.parse_var_declaration())
            else:
                break
        return declarations

    def parse_var_declaration(self):
        # <ID> {, <ID>} : <type>
        vars = [self.parse_identifier()]
        while self.check_type("DELIMITER") and self.check_value(","):
            self.eat("DELIMITER", ",")
            vars.append(self.parse_identifier())
        self.eat("DELIMITER", ":")
        var_type = self.parse_type()
        return ("VarDecl", vars, var_type)

    def parse_type(self):
        # integer | real | boolean
        if self.check_type("ID"):
            t = self.current_token[1]
            if t in ["integer", "real", "boolean"]:
                self.eat("ID")
                return t
            else:
                self.error("Unknown type")
        else:
            self.error("Type expected")

    def parse_compound_statement(self):
        # begin <statement_list> end
        if self.check_type("KEYWORD") and self.check_value("begin"):
            self.eat("KEYWORD", "begin")
            stmts = self.parse_statement_list()
            self.eat("KEYWORD", "end")
            return ("Compound", stmts)
        else:
            self.error("Expected 'begin' for compound statement")

    def parse_statement_list(self):
        stmts = []
        stmts.append(self.parse_statement())
        while self.check_type("DELIMITER") and self.current_token[1] == ";":
            self.eat("DELIMITER", ";")
            if self.current_token and (
                self.check_type("ID") or
                (self.check_type("KEYWORD") and self.current_token[1] in ["if","while","for","readln","write","begin"])):
                stmts.append(self.parse_statement())
            else:
                break
        return stmts

    def parse_statement(self):
        if self.check_type("ID"):
            return self.parse_assign_statement()
        elif self.check_type("KEYWORD"):
            kw = self.current_token[1]
            if kw == "if":
                return self.parse_if_statement()
            elif kw == "while":
                return self.parse_while_statement()
            elif kw == "for":
                return self.parse_for_statement()
            elif kw == "readln":
                return self.parse_readln_statement()
            elif kw == "write":
                return self.parse_write_statement()
            elif kw == "begin":
                return self.parse_compound_statement()
            else:
                self.error("Unexpected keyword in statement")
        else:
            self.error("Statement expected")

    def parse_assign_statement(self):
        # <ID> := <expression>
        var_name = self.parse_identifier()
        self.eat("ASSIGN", ":=")
        expr = self.parse_expression()
        return ("Assign", var_name, expr)

    def parse_if_statement(self):
        # if <expression> then <statement> [else <statement>]
        self.eat("KEYWORD", "if")
        cond = self.parse_expression()
        self.eat("KEYWORD", "then")
        true_stmt = self.parse_statement()
        false_stmt = None
        if self.check_type("KEYWORD") and self.check_value("else"):
            self.eat("KEYWORD", "else")
            false_stmt = self.parse_statement()
        return ("If", cond, true_stmt, false_stmt)

    def parse_while_statement(self):
        # while <expression> do <statement>
        self.eat("KEYWORD", "while")
        cond = self.parse_expression()
        if self.check_type("KEYWORD") and self.check_value("do"):
            self.eat("KEYWORD", "do")
        else:
            self.error("Expected 'do' after while condition")
        stmt = self.parse_statement()
        return ("While", cond, stmt)

    def parse_for_statement(self):
        # for <ID> := <expression> to <expression> do <statement>
        self.eat("KEYWORD", "for")
        var_name = self.parse_identifier()
        self.eat("ASSIGN", ":=")
        start_expr = self.parse_expression()
        self.eat("KEYWORD", "to")
        end_expr = self.parse_expression()
        if self.check_type("KEYWORD") and self.check_value("do"):
            self.eat("KEYWORD", "do")
        else:
            self.error("Expected 'do' in for statement")
        stmt = self.parse_statement()
        return ("For", var_name, start_expr, end_expr, stmt)

    def parse_readln_statement(self):
        # readln ( <ID> )
        self.eat("KEYWORD", "readln")
        self.eat("DELIMITER", "(")
        var_name = self.parse_identifier()
        self.eat("DELIMITER", ")")
        return ("Readln", var_name)

    def parse_write_statement(self):
        # write ( <expression> )
        self.eat("KEYWORD", "write")
        self.eat("DELIMITER", "(")
        expr = self.parse_expression()
        self.eat("DELIMITER", ")")
        return ("Write", expr)

    def parse_expression(self):
        # <simple_expression> { <rel_op> <simple_expression> }
        node = self.parse_simple_expression()
        while self.check_type("REL_OP"):
            op = self.current_token[1]
            self.eat("REL_OP")
            right = self.parse_simple_expression()
            node = ("BinOp", op, node, right)
        return node

    def parse_simple_expression(self):
        # <term> { (+|-|or) <term> }
        node = self.parse_term()
        while (self.check_type("ADD_OP") or
               (self.check_type("KEYWORD") and self.current_token[1] == "or")):
            op = self.current_token[1]
            self.eat(self.current_token[0])
            right = self.parse_term()
            node = ("BinOp", op, node, right)
        return node

    def parse_term(self):
        # <factor> { (*|/|and) <factor> }
        node = self.parse_factor()
        while (self.check_type("MUL_OP") or
               (self.check_type("KEYWORD") and self.current_token[1] == "and")):
            op = self.current_token[1]
            self.eat(self.current_token[0])
            right = self.parse_factor()
            node = ("BinOp", op, node, right)
        return node

    def parse_factor(self):
        # <идентификатор> | <число> | <строка> | true | false | ( <выражение> ) | not <фактор>
        if self.check_type("ID"):
            var_name = self.current_token[1]
            self.eat("ID")
            return ("Var", var_name)
        elif self.check_type("NUMBER"):
            val = self.current_token[1]
            self.eat("NUMBER")
            return ("Number", val)
        elif self.check_type("STRING"):
            val = self.current_token[1]
            self.eat("STRING")
            return ("String", val)
        elif self.check_type("KEYWORD") and self.current_token[1] == "true":
            self.eat("KEYWORD", "true")
            return ("Boolean", True)
        elif self.check_type("KEYWORD") and self.current_token[1] == "false":
            self.eat("KEYWORD", "false")
            return ("Boolean", False)
        elif self.check_type("DELIMITER") and self.current_token[1] == "(":
            self.eat("DELIMITER", "(")
            expr = self.parse_expression()
            self.eat("DELIMITER", ")")
            return expr
        elif self.check_type("KEYWORD") and self.current_token[1] == "not":
            self.eat("KEYWORD", "not")
            factor = self.parse_factor()
            return ("Not", factor)
        else:
            self.error("Factor expected")

    def parse_identifier(self):
        if self.check_type("ID"):
            id_name = self.current_token[1]
            self.eat("ID")
            return id_name
        else:
            self.error("Identifier expected")
