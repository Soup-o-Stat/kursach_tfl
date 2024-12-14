global_type=None

class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []

    def analyze(self, operations):
        print("Начало семантического анализа...")
        for operation in operations:
            print(f"Обрабатываем операцию: {operation}")
            if operation[0] == 'assign':
                variable = operation[1]
                print(f"Проверяем переменную для присваивания: {variable}")
                if variable not in self.symbol_table:
                    self.errors.append(f"Ошибка: Переменная '{variable}' не объявлена.")
            elif operation[0] == 'use':
                variable = operation[1]
                print(f"Проверяем использование переменной: {variable}")
                if variable not in self.symbol_table:
                    self.errors.append(f"Ошибка: Переменная '{variable}' не объявлена.")
            else:
                self.errors.append(f"Ошибка: Неизвестная операция '{operation[0]}'.")
            print(f"Текущие ошибки: {self.errors}")
        print("Семантический анализ завершен.")
        return self.errors

    def get_errors(self):
        return self.errors

def generate_symbol_table_and_operations(tokens):
    global global_type
    symbol_table = {}
    operations = []
    current_type = None
    in_var_section = False
    var_seen = False
    begin_seen = False

    for j, token in enumerate(tokens):
        print(f"Обрабатываем токен: {token}")
        if token[0] == 'KEYWORD':
            if token[1] in ['integer', 'real', 'boolean']:
                current_type = token[1]
                global_type=token[1]
                print(current_type)

    for i, token in enumerate(tokens):
        print(f"Обрабатываем токен: {token}")
        if token[0] == 'KEYWORD':
            if token[1] == 'var':
                var_seen = True
                in_var_section = True
            elif token[1] in ['integer', 'real', 'boolean'] and var_seen and not begin_seen:
                current_type = token[1]
            elif token[1] == 'begin':
                begin_seen = True
                in_var_section = False
                current_type = None
        elif token[0] == 'ID' and var_seen and not begin_seen:
            if token[1] not in symbol_table:
                # if current_type==None:
                #     if token[1]=="real":
                #         global_type = token[1]
                #     if token[1]=="integer":
                #         global_type=token[1]
                symbol_table[token[1]] = {'type': current_type, 'scope': 'global'}
                print(global_type)
                print(f"Переменная '{token[1]}' добавлена в таблицу символов с типом '{current_type}'")
        elif token[0] == 'ID' and not in_var_section:
            if token[1] not in symbol_table:
                operations.append(('use', token[1]))
                print(f"Переменная '{token[1]}' используется, но не найдена в таблице символов.")
            else:
                operations.append(('use', token[1]))
                print(f"Переменная '{token[1]}' используется и найдена в таблице символов.")
        # elif token[0]=="NUMBER":
        #     for i in token[1]:
        #         if i not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
        #             print(i)
        #             raise SyntaxError(f"Неожиданное число: {token[1]}")
        #         if i=="." and current_type!="real":
        #             # raise SyntaxError(f"Неправильный тип: {current_type}")
        #             print(current_type)
        #             print()
        #             print()
        elif token[0] == 'ASSIGN':
            if i > 0 and tokens[i - 1][0] == 'ID':
                var_name = tokens[i - 1][1]
                if var_name not in symbol_table:
                    operations.append(('assign', var_name))
                    print(f"Переменная '{var_name}' используется для присваивания, но не найдена в таблице символов.")
                else:
                    operations.append(('assign', var_name))
                    print(f"Переменная '{var_name}' используется для присваивания и найдена в таблице символов.")

    for pencil, token in enumerate(tokens):
        if token[0]=="NUMBER":
            for i in token[1]:
                print(global_type)
                if i not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "true", "false"]:
                    print(i)
                    raise SyntaxError(f"Неожиданное число: {token[1]}")
                if i=="." and global_type!="real":
                    raise SyntaxError(f"Неправильный тип: {global_type}")
                    # print(current_type)
                    # print()
                    # print()

    print(f"Таблица символов: {symbol_table}")
    return symbol_table, operations