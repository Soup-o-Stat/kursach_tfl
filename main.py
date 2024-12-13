from lexer import LexicalAnalyzer
from parserr import SyntaxAnalyzer
from semantic import SemanticAnalyzer, generate_symbol_table_and_operations

code = [
    '''
    {программа 1}
    program
    var x, y : integer; 
    begin
      x := 5;  { Присваиваем x значение 5 }
      y := 10; { Присваиваем y значение 10 }

      if x < y then [
        write (x);
        write (y);
      ]
      else [
        write (y);
        write (x);
      ]
    end.
    ''',

    '''
    program
    var 
    a, b, c : real;
    begin
      a := 3;
      pizda := 2;
      c := a * b;
      if c > 10 then [
        write(c);
      ]
    end.
    '''
]

for i, program in enumerate(code, start=1):
    print(f"Программа {i}:")
    print("* Лексический анализ *")
    lexer = LexicalAnalyzer(program)
    tokens = lexer.tokenize()
    for token in tokens:
        print(f"Токен: {token[0]}, элемент: {token[1]}")
    print("* Лексический анализ завершен *")

    print("* Синтаксический анализ *")
    try:
        parser = SyntaxAnalyzer(tokens)
        parsed_program = parser.parse()
        print(f"Синтаксический анализ завершен. Статус: {parsed_program}")

        print("* Семантический анализ *")
        symbol_table, operations = generate_symbol_table_and_operations(tokens)
        analyzer = SemanticAnalyzer(symbol_table)
        analyzer.analyze(operations)
        errors = analyzer.get_errors()
        if errors:
            print("Обнаружены ошибки семантического анализа:")
            for error in errors:
                print(error)
        else:
            print("Семантический анализ успешно завершен. Ошибок нет.")

    except Exception as e:
        print(f"Ошибка синтаксического анализа: {e}")
    print("------------------------")
