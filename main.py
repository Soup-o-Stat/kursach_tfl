from lexer import LexicalAnalyzer
from parserr import Parser

code = [
    '''
    program
    var x, y : integer; 
    begin
      x := 5;  { Присваиваем x значение 5 }
      y := 10; { Присваиваем y значение 10 }

      if x < y then [
        write (x);
        write (x, y);
      ]
      else [
        write (y);
        write (y, x);
      ]
    end.
    ''',

    '''
    program
    var a, b, c : real;
    begin
      a := 3.14;
      b := 2.71;
      c := a * b;
      if c > 10 then [
        write(c);
      ]
      else [
        write("Too small");
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
        parser = Parser(tokens)
        parsed_program = parser.parse_program()
        print(f"Синтаксический анализ завершен: {parsed_program}")
    except Exception as e:
        print(f"Ошибка синтаксического анализа: {e}")
    print("------------------------")
