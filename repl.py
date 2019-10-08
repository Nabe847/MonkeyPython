import pmonkey.lexer as lexer
import pmonkey.parser as parser
import pmonkey.token as token
import pmonkey.evaluator as evaluator
from pmonkey.environment import Environment

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
    env = Environment()
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

        evaluated = evaluator.eval(program, env)
        if evaluated != None:
            print(evaluated.inspect())


if __name__ == "__main__":
    start()
