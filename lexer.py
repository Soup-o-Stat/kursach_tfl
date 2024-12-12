from enum import Enum

class LexicalAnalyzer:
    class State(Enum):
        H = "H"  # Начальное состояние
        ID = "ID"  # Идентификаторы
        NUM = "NUM"  # Числа
        COM = "COM"  # Комментарии
        ALE = "ALE"  # Операции отношения
        NEQ = "NEQ"  # Неравенство
        DELIM = "DELIM"  # Разделители
        STR = "STR"  # Строковые литералы

    # Ключевые слова
    TW = [
        "program", "var", "begin", "end", "if", "else", "while", "for", "to", "then", "next", "as",
        "readln", "write", "true", "false", "%", "!", "$", "end_else"
    ]

    # Разделители и операторы
    TD = [
        "[", "]", "{", "}", "(", ")", ",", ":", ";", ":=", ".", "+", "-", "*", "/", "and", "/", "not",
        "!=", "==", "<", "<=", ">", ">="
    ]

    def __init__(self, input_text):
        self.text = input_text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None
        self.tokens = []
        self.before_begin = True

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def add_token(self, type_, value):
        self.tokens.append((type_, value))

    def clear_whitespace(self):
        while self.current_char and self.current_char in ' \n\r\t':
            self.advance()

    def parse_identifier_or_keyword(self):
        start = self.pos
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        text = self.text[start:self.pos]
        if text in self.TW:
            self.add_token('KEYWORD', text, )
            if text == 'begin':
                self.before_begin = False
        else:
            self.add_token('ID', text, )

    def parse_number(self):
        start = self.pos
        base_detected = False

        # Проверка на основание числа
        if self.current_char == '0':
            self.advance()
            if self.current_char in 'Bb':  # Binary
                base_detected = True
                self.advance()
                while self.current_char and self.current_char in '01':
                    self.advance()
            elif self.current_char in 'Oo':  # Octal
                base_detected = True
                self.advance()
                while self.current_char and self.current_char in '01234567':
                    self.advance()
            elif self.current_char in 'Xx':  # Hexadecimal
                base_detected = True
                self.advance()
                while self.current_char and (self.current_char.isdigit() or self.current_char.upper() in 'ABCDEF'):
                    self.advance()

        if not base_detected:
            while self.current_char and self.current_char.isdigit():
                self.advance()
            if self.current_char == '.':
                self.advance()
                while self.current_char and self.current_char.isdigit():
                    self.advance()
            if self.current_char and self.current_char.upper() == 'E':
                self.advance()
                if self.current_char in '+-':
                    self.advance()
                if self.current_char and self.current_char.isdigit():
                    while self.current_char and self.current_char.isdigit():
                        self.advance()
                else:
                    self.add_token('ERROR', self.text[start:self.pos], )
                    return
        if self.current_char in 'bohBOH':
            suffix = self.current_char.lower()
            self.advance()
            self.add_token('NUMBER', self.text[start:self.pos] + suffix, )
        else:
            text = self.text[start:self.pos]
            self.add_token('NUMBER', text, )

    def parse_string(self):
        self.advance()
        start = self.pos
        while self.current_char and self.current_char != "'":
            self.advance()
        text = self.text[start:self.pos]
        self.add_token('STRING', f"'{text}'", )
        self.advance()

    def parse_comment(self):
        self.advance()
        while self.current_char and self.current_char != '}':
            self.advance()
        self.advance()

    def parse_delimiter_or_operator(self):
        start = self.pos
        self.advance()
        if self.current_char and (self.text[start:self.pos + 1] in self.TD):
            self.advance()
        text = self.text[start:self.pos]
        if text in ["==", "!=", "<", "<=", ">", ">="]:
            self.add_token('REL_OP', text, )
        elif text in ["+", "-", "||"]:
            self.add_token('ADD_OP', text, )
        elif text in ["*", "/", "&&"]:
            self.add_token('MUL_OP', text, )
        elif text == ":=":
            self.add_token('ASSIGN', text, )
        elif text in self.TD:
            self.add_token('DELIMITER', text, )
        else:
            self.add_token('UNKNOWN', text, )

    def tokenize(self):
        while self.current_char:
            self.clear_whitespace()
            if not self.current_char:
                break
            if self.current_char.isalpha():
                self.parse_identifier_or_keyword()
            elif self.current_char.isdigit():
                self.parse_number()
            elif self.current_char == "'":
                self.parse_string()
            elif self.current_char == '{':
                self.parse_comment()
            elif self.current_char == '!':
                if self.text[self.pos:self.pos + 2] == "!=":
                    self.add_token('REL_OP', '!=', )
                    self.advance()
                    self.advance()
                else:
                    if self.before_begin:
                        self.add_token('KEYWORD', '!', )
                    else:
                        self.add_token('DELIMITER', '!', )
                    self.advance()
            elif self.current_char in "%$":
                self.add_token('KEYWORD', self.current_char, )
                self.advance()
            elif self.current_char in self.TD:
                self.parse_delimiter_or_operator()
            else:
                self.add_token('UNKNOWN', self.current_char, )
                self.advance()
        return self.tokens