from dataclasses import dataclass
@dataclass
class Token:
    kind: str; value: object; position: int; line: int
KEYWORDS = {"let","print","if","else","while","function","return","true","false","and","or","end"}
SINGLE_CHAR = {"+":"PLUS","-":"MINUS","*":"STAR","/":"SLASH","(":"LPAREN",")":"RPAREN",",":"COMMA","{":"LBRACE","}":"RBRACE",";":"SEMICOLON",":":"COLON","=":"EQUALS",">":"GREATER","<":"LESS","!":"BANG"}
TWO_CHAR = {"==":"EQUAL_EQUAL","!=":"NOT_EQUAL",">=":"GREATER_EQUAL","<=":"LESS_EQUAL"}
