from collections import deque

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.popleft()
            next_token = self.tokens[0] if self.tokens else None
            print(f"Текущий токен: {self.current_token}, следующий токен: {next_token}")
            if self.current_token[0]=="NUMBER" and next_token[0]=="ID":
                raise SyntaxError(f"Неожиданный оператор: {self.current_token[1]}{next_token[1]}")

        else:
            self.current_token = None
            print("Токены закончились.")

    def parse(self):
        print("Начинаем синтаксический анализ...")
        self.program()
        if self.current_token is not None:
            raise SyntaxError(f"Неожиданный токен: {self.current_token}")
        return "OK"

    def program(self):
        print(f"Начинаем разбор программы, текущий токен: {self.current_token}")
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'program':
            self.next_token()
            self.block()
        else:
            raise SyntaxError("Ожидалось 'program'.")

    def block(self):
        print(f"Проверка токена в блоке: {self.current_token}")
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'var':
            self.variable_declarations()
        found_begin = False
        while self.current_token is not None:
            if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'begin':
                found_begin = True
                self.next_token()
                break
            self.next_token()
        if not found_begin:
            raise SyntaxError("Ожидалось 'begin' после объявления переменных.")
        self.statements()
        print(f"Текущий токен перед 'end': {self.current_token}")
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'end':
            self.next_token()
            if self.current_token[0] == 'DELIMITER' and self.current_token[1] == '.':
                self.next_token()
            else:
                raise SyntaxError("Ожидалась точка '.' после 'end'.")
        else:
            raise SyntaxError("Ожидалось 'end' после блока.")

    def variable_declarations(self):
        print(f"Начинаем разбор объявлений переменных.")
        while self.current_token[0] == 'ID':
            print(f"Обрабатываем переменную: {self.current_token[1]}")
            self.next_token()
            if self.current_token[0] == 'DELIMITER' and self.current_token[1] == ',':
                self.next_token()
            elif self.current_token[0] == 'DELIMITER' and self.current_token[1] == ';':
                self.next_token()
                break
            else:
                raise SyntaxError("Ожидалось ',' или ';' после объявления переменной.")

    def statements(self):
        print(f"Начинаем разбор операторов.")
        while self.current_token is not None and (self.current_token[0] != 'KEYWORD' or self.current_token[1] != 'end'):
            if self.current_token[0] == 'ID' and self.tokens and self.tokens[0][1] == ':=':
                print("Обрабатываем оператор присваивания.")
                self.assignment_statement()
            elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'if':
                print("Обрабатываем условие 'if'.")
                self.if_statement()
            elif self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'while':
                print("Обрабатываем условие 'while'.")
                self.while_statement()
            else:
                raise SyntaxError(f"Неожиданный оператор: {self.current_token}")

    def assignment_statement(self):
        print(f"Обрабатываем оператор присваивания: {self.current_token[1]}")
        var_name = self.current_token[1]
        self.next_token()
        if self.current_token[0] == 'ASSIGN' and self.current_token[1] == ':=':
            self.next_token()
            self.expression()
            if self.current_token[0] == 'DELIMITER' and self.current_token[1] == ';':
                self.next_token()
            else:
                raise SyntaxError("Ожидался символ ';' после присваивания.")
        else:
            raise SyntaxError("Ожидалось ':=' в операторе присваивания.")

    def expression(self):
        print(f"Обрабатываем выражение с текущим токеном: {self.current_token}")
        self.term()
        while self.current_token is not None and self.current_token[0] in ['ADD_OP', 'SUB_OP']:
            print(f"Обрабатываем операцию: {self.current_token[1]}")
            self.next_token()
            self.term()

    def term(self):
        print(f"Обрабатываем терм с текущим токеном: {self.current_token}")
        self.factor()
        while self.current_token is not None and self.current_token[0] in ['MUL_OP', 'DIV_OP']:
            print(f"Обрабатываем операцию: {self.current_token[1]}")
            self.next_token()
            self.factor()

    def factor(self):
        print(f"Обрабатываем фактор с текущим токеном: {self.current_token}")
        if self.current_token[0] == 'ID' or self.current_token[0] == 'NUMBER':
            self.next_token()
        else:
            raise SyntaxError(f"Неожиданный токен в факторе: {self.current_token}")

    def write_statement(self):
        print(f"Обрабатываем оператор write с текущим токеном: {self.current_token}")
        self.next_token()
        if self.current_token[0] == 'DELIMITER' and self.current_token[1] == '(':
            self.next_token()
            self.expression()
            if self.current_token[0] == 'DELIMITER' and self.current_token[1] == ')':
                self.next_token()
            else:
                raise SyntaxError("Ожидалась закрывающая скобка ')' после аргумента write.")
        else:
            raise SyntaxError("Ожидалась открывающая скобка '(' после write.")

    def if_statement(self):
        print(f"Обрабатываем оператор 'if' с текущим токеном: {self.current_token}")
        self.next_token()
        self.expression()
        if self.current_token[0] == 'REL_OP' and self.current_token[1] in ['>', '<', '=', '>=', '<=']:
            self.next_token()
            self.next_token()
            if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'then':
                self.next_token()
                if self.current_token[0] == 'DELIMITER' and self.current_token[1] == '[':
                    self.next_token()
                    while self.current_token[0] != 'DELIMITER' or self.current_token[1] != ']':
                        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'write':
                            self.write_statement()
                        elif self.current_token[0] == 'DELIMITER' and self.current_token[1] == ';':
                            self.next_token()
                        else:
                            self.statements()
                    if self.current_token[0] == 'DELIMITER' and self.current_token[1] == ']':
                        self.next_token()
                    else:
                        raise SyntaxError("Ожидался закрывающий ']' после блока операторов.")
                else:
                    raise SyntaxError("Ожидался блок операторов после 'then'.")
                if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'else':
                    self.next_token()
                    if self.current_token[0] == 'DELIMITER' and self.current_token[1] == '[':
                        self.next_token()
                        while self.current_token[0] != 'DELIMITER' or self.current_token[1] != ']':
                            if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'write':
                                self.write_statement()
                            elif self.current_token[0] == 'DELIMITER' and self.current_token[1] == ';':
                                self.next_token()
                            else:
                                self.statements()
                        if self.current_token[0] == 'DELIMITER' and self.current_token[1] == ']':
                            self.next_token()
                        else:
                            raise SyntaxError("Ожидался закрывающий ']' после блока операторов в 'else'.")
                    else:
                        self.statements()
            else:
                raise SyntaxError("Ожидалось 'then' после условия 'if'.")
        else:
            raise SyntaxError("Ожидался оператор сравнения после условия 'if'.")

    def while_statement(self):
        print(f"Обрабатываем оператор 'while' с текущим токеном: {self.current_token}")
        self.next_token()
        self.expression()
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'do':
            self.next_token()
            self.statements()
        else:
            raise SyntaxError("Ожидалось 'do' после условия 'while'.")
