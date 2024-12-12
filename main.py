from lexer import LexicalAnalyzer

# from parserr import Parser

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

for i in code:
    print("Лексический анализ")
    lexer = LexicalAnalyzer(i)
    tokens = lexer.tokenize()
    for j in tokens:
        print(j)
    print("Лексический анализ завершен")
    print()
    print()
    # print("Синтаксический анализ")
    # try:
    #     parser = Parser(tokens)
    #     parser.parse_program()
    #     print("Синтаксический анализ завершен")
    # except SyntaxError as e:
    #     print(f"Ошибка синтаксического анализа: {e}")
    print("------------------------")
    print()
    print()
