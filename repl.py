import lexer
import monkey_token

PROMPT = ">> "


def start():
    while True:
        print(PROMPT, end='')
        source = input()

        if not source:
            return

        lex = lexer.Lexer(source)

        while(True):
            tok = lex.next_token()
            print(tok)

            if tok.token_type == monkey_token.EOF:
                break
