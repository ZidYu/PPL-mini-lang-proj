from .tokens import Token, KEYWORDS, SINGLE_CHAR, TWO_CHAR
class LexerError(Exception): pass
class Lexer:
    def __init__(self, source): self.source=source; self.i=0; self.line=1
    def scan(self):
        out=[]
        while self.i<len(self.source):
            c=self.source[self.i]
            if c in ' \t\r': self.i+=1; continue
            if c=='\n': self.line+=1; self.i+=1; continue
            if c=='#' or (c=='/' and self.i+1<len(self.source) and self.source[self.i+1]=='/'):
                while self.i<len(self.source) and self.source[self.i]!='\n': self.i+=1
                continue
            pos=self.i; line=self.line; pair=self.source[self.i:self.i+2]
            if pair in TWO_CHAR: out.append(Token(TWO_CHAR[pair],pair,pos,line)); self.i+=2; continue
            if c in SINGLE_CHAR: out.append(Token(SINGLE_CHAR[c],c,pos,line)); self.i+=1; continue
            if c=='"': out.append(Token('STRING',self._string(),pos,line)); continue
            if c.isdigit(): out.append(Token('NUMBER',self._number(),pos,line)); continue
            if c.isalpha() or c=='_':
                word=self._identifier(); out.append(Token(word.upper() if word in KEYWORDS else 'IDENTIFIER',word,pos,line)); continue
            raise LexerError(f"Illegal character '{c}' at line {line}, position {pos}")
        out.append(Token('EOF',None,self.i,self.line)); return out
    def _number(self):
        start=self.i
        while self.i<len(self.source) and self.source[self.i].isdigit(): self.i+=1
        if self.i<len(self.source) and self.source[self.i]=='.':
            self.i+=1
            if self.i>=len(self.source) or not self.source[self.i].isdigit(): raise LexerError(f'Invalid number at line {self.line}')
            while self.i<len(self.source) and self.source[self.i].isdigit(): self.i+=1
            return float(self.source[start:self.i])
        return int(self.source[start:self.i])
    def _string(self):
        self.i+=1; chars=[]
        while self.i<len(self.source) and self.source[self.i]!='"':
            if self.source[self.i]=='\n': self.line+=1
            chars.append(self.source[self.i]); self.i+=1
        if self.i>=len(self.source): raise LexerError(f'Unterminated string at line {self.line}')
        self.i+=1; return ''.join(chars)
    def _identifier(self):
        start=self.i
        while self.i<len(self.source) and (self.source[self.i].isalnum() or self.source[self.i]=='_'): self.i+=1
        return self.source[start:self.i]
