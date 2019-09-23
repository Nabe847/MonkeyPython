import pmonkey.lexer as lexer
import pmonkey.parser as parser
import pmonkey.token as token

PROMPT = ">> "

MONKEY_FACE = r"""
            __,__
   .--.  .-"     "-.  .--.
  / .. \/  .-. .-.  \/ .. \
 | |  '|  /   Y   \  |'  | |
 | \   \  \ 0 | 0 /  /   / |
  \ '- ,\.-"""""""-./, -' /
   ''-' /_   ^ ^   _\ '-''
       |  \._   _./  |
       \   \ '~' /   /
        '._ '-=-' _.'
           '-----'
"""

def start():
    while True:
        print(PROMPT, end='')
        source = input()

        if not source or source == "exit":
            return

        lex = lexer.Lexer(source)
        psr = parser.Parser(lex)
        program = psr.parse_program()

        if len(psr.errors) > 0:
            print(MONKEY_FACE)
            print("Woops! We ran into some monkey business here!")
            print("parser errors:")
            print("\n".join([str(e) for e in psr.errors]))
            continue

        print(program)
        print()

if __name__ == "__main__":
    start()
