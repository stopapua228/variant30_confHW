from .lexer import Lexer,LexError,Token
from .lexer import TT_NUMBER,TT_IDENT,TT_LPAREN,TT_RPAREN,TT_EQ,TT_LET,TT_LIST,TT_CONSTREF,TT_EOF

class ParseError(Exception):
    def __init__(self,message,line,col):
        super().__init__(f"{message} at line {line}, col {col}")
        self.line=line
        self.col=col

class Parser:
    def __init__(self,src):
        self.lex=Lexer(src)
        self.tok=self.lex.next()
        self.consts={}

    def _err(self,msg):
        raise ParseError(msg,self.tok.line,self.tok.col)

    def _eat(self,typ):
        if self.tok.type!=typ:
            self._err(f"Expected {typ}, got {self.tok.type}")
        self.tok=self.lex.next()

    def parse(self):
        while self.tok.type==TT_LET:
            self._parse_let()
        root=self._parse_value()
        if self.tok.type!=TT_EOF:
            self._err("Unexpected token after root value")
        return root

    def _parse_let(self):
        self._eat(TT_LET)
        if self.tok.type!=TT_IDENT:
            self._err("Expected identifier after let")
        name=self.tok.value
        self._eat(TT_IDENT)
        self._eat(TT_EQ)
        val=self._parse_value()
        self.consts[name]=self._deepcopy(val)

    def _parse_value(self):
        if self.tok.type==TT_NUMBER:
            v=self.tok.value
            self._eat(TT_NUMBER)
            return v
        if self.tok.type==TT_CONSTREF:
            name=self.tok.value
            line=self.tok.line
            col=self.tok.col
            self._eat(TT_CONSTREF)
            if name not in self.consts:
                raise ParseError(f"Undeclared constant '{name}'",line,col)
            return self._deepcopy(self.consts[name])
        if self.tok.type==TT_LPAREN:
            return self._parse_list()
        self._err("Expected value")

    def _parse_list(self):
        self._eat(TT_LPAREN)
        if self.tok.type!=TT_LIST:
            self._err("Expected 'list' after '('")
        self._eat(TT_LIST)
        items=[]
        while self.tok.type!=TT_RPAREN:
            if self.tok.type==TT_EOF:
                self._err("Unexpected end of file, expected ')'")
            items.append(self._parse_value())
        self._eat(TT_RPAREN)
        return items

    def _deepcopy(self,v):
        if isinstance(v,list):
            return [self._deepcopy(x) for x in v]
        return v

def compile_to_value(src):
    p=Parser(src)
    return p.parse()
