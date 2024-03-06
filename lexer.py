# TODO:
#

import keyword, string

# Sets for checking input characters
letters = set(string.ascii_letters + "_")
digits = set(string.digits)
keywords = set(keyword.kwlist)
operators = {"+","-","*","/","%","//","==","!=",">","<",">=","<=","=","+=","-=","*=",
             "/=","%=","**=","//=","&","|","^","~","<<",">>",}
separators = {"(", ")", "[", "]", "{", "}", ",", ";", ":", ".", "@", "#", '"', "'"}
whitespace = {" ", "\t", "\n"}

# Constants for token types
INTEGER, IDENTIFIER, KEYWORD, OPERATOR, SEPARATOR, REAL = (
    "Integer",
    "Identifier",
    "Keyword",
    "Operator",
    "Separator",
    "Real",
)

class Token:
    def __init__(self, type, lexeme):
        self.type = type
        self.lexeme = lexeme

    def __repr__(self):
        return f"{self.type:<10} | {self.lexeme}"

class Lexer:
    def __init__(self, filename):
        try:
            with open(filename, "r") as file:
                self.input = file.read()
        except IOError as e:
            print(f"Could not open or read file: {filename}")
            self.input = ""
        self.position = 0
        self.current_char = self.input[self.position] if self.input else None

    def get_next_char(self):
        """Advances position and reads next character"""
        self.position += 1
        if self.position < len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None

    def next_token(self):
        """Lexical analyzer (tokenizer) to get the next token."""
        while self.current_char is not None:
            if self.current_char in whitespace:
                self.get_next_char()  # Skip whitespace characters
                continue
            elif (
                self.current_char in letters
            ):  # if char is a letter, call identifier fsm, then check if keyword
                token = self.identifier_fsm()
                if token.lexeme in keywords:
                    token.type = KEYWORD
                return token
            elif self.current_char in digits:  # if char is a digit, call integer fsm
                return self.integer_fsm()
            elif self.current_char in operators:
                operator = self.current_char
                self.get_next_char()
                if self.current_char in operators:  # double digit operator check
                    operator += self.current_char
                    self.get_next_char()
                return Token(OPERATOR, operator)
            elif self.current_char in separators:  # single character separators
                separator = self.current_char
                self.get_next_char()
                return Token(SEPARATOR, separator)
            else:
                self.get_next_char()
        return None  # Indicates end of input or no more tokens

    def identifier_fsm(self):
        """Finite State Machine for recognizing identifiers."""
        state = 1
        accepting_states = [2]
        identifier = ""
        identifier_transition_table = {
            (1, "letter"): 2,
            (2, "letter"): 2,
            (2, "digit"): 2,
        }
        while self.current_char is not None:
            char_category = (
                "letter"
                if self.current_char in letters
                else "digit" if self.current_char in digits else "other"
            )
            if (state, char_category) in identifier_transition_table:
                state = identifier_transition_table[(state, char_category)]
                identifier += self.current_char
            else:
                break  # Exit loop if no valid transition
            self.get_next_char()

        if state in accepting_states:
            return Token(IDENTIFIER, identifier)
        else:
            return None

    def integer_fsm(self):
        """Finite State Machine for recognizing integers and reals"""
        state = 1
        accepting_states = [2, 4]
        integer_or_real = ""
        integer_transition_table = {
            (1, "digit"): 2,
            (2, "digit"): 2,
            (2, "."): 3,
            (3, "digit"): 4,
            (4, "digit"): 4,
        }
        while self.current_char is not None:
            char_category = (
                "."
                if self.current_char == "."
                else "digit" if self.current_char in digits else "other"
            )
            if (state, char_category) in integer_transition_table:
                state = integer_transition_table[(state, char_category)]
                integer_or_real += self.current_char
            else:
                break  # Exit loop if no valid transition
            self.get_next_char()

        if state == 2:
            return Token(INTEGER, integer_or_real)
        elif state == 4:
            return Token(REAL, integer_or_real)
        else:
            return None

    def output_tokens(self, tokens, output_file):
        """Formatted output of tokens and lexemes to output file"""
        with open(output_file, "w") as file:
            file.write(f"{'Token':<10} | Lexeme\n")
            file.write("-" * 30 + "\n")
            for token in tokens:
                file.write(f"{token}\n")
        print(f"Output written to: {output_file}")

# Example usage:
input_file = input("Enter the input file name: ")
lexer = Lexer(input_file)
tokens = []
while True:
    token = lexer.next_token()
    if token is None:
        break
    tokens.append(token)
lexer.output_tokens(tokens, "output.txt")
