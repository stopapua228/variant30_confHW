import re

TT_NUMBER="NUMBER"
TT_IDENT="IDENT"
TT_LPAREN="LPAREN"
TT_RPAREN="RPAREN"
TT_EQ="EQ"
TT_LET="LET"
TT_LIST="LIST"
TT_CONSTREF="CONSTREF"
TT_EOF="EOF"

_ident_re=re.compile(r"^[a-z][a-z0-9_]*$")

class LexError(Exception):
    def __init__(self,message,line,col):
        super().__init__(f"{message} at line {line}, col {col}")
        self.line=line
        self.col=col

class Token:
    __slots__=("type","value","line","col")
    def __init__(self,typ,value,line,col):
        self.type=typ
        self.value=value
        self.line=line
        self.col=col

class Lexer:
    def __init__(self,src):
        self.src=src.replace("\r\n","\n").replace("\r","\n")
        self.n=len(self.src)
        self.i=0
        self.line=1
        self.col=1

    def _peek(self,off=0):
        j=self.i+off
        if j>=self.n:
            return ""
        return self.src[j]

    def _adv(self):
        ch=self._peek()
        if ch=="":
            return ""
        self.i+=1
        if ch=="\n":
            self.line+=1
            self.col=1
        else:
            self.col+=1
        return ch

    def _skip_ws_and_comments(self):
        while True:
            while self._peek() and self._peek().isspace():
                self._adv()
            if self._peek()=="R" and self.src[self.i:self.i+3]=="REM":
                nxt=self._peek(3)
                if nxt=="" or nxt.isspace():
                    while self._peek() and self._peek()!="\n":
                        self._adv()
                    continue
            break

    def next(self):
        self._skip_ws_and_comments()
        if self.i>=self.n:
            return Token(TT_EOF,"",self.line,self.col)

        ch=self._peek()
        start_line=self.line
        start_col=self.col

        if ch.isdigit():
            j=self.i
            while self._peek() and self._peek().isdigit():
                self._adv()
            return Token(TT_NUMBER,int(self.src[j:self.i]),start_line,start_col)

        if ch.isalpha():
            j=self.i
            while True:
                c=self._peek()
                if not c or not (c.isalnum() or c=="_"):
                    break
                self._adv()
            word=self.src[j:self.i]
            if word=="let":
                return Token(TT_LET,word,start_line,start_col)
            if word=="list":
                return Token(TT_LIST,word,start_line,start_col)
            if _ident_re.fullmatch(word):
                return Token(TT_IDENT,word,start_line,start_col)
            raise LexError(f"Invalid identifier '{word}'",start_line,start_col)

        if ch=="(":
            self._adv()
            return Token(TT_LPAREN,"(",start_line,start_col)
        if ch==")":
            self._adv()
            return Token(TT_RPAREN,")",start_line,start_col)
        if ch=="=":
            self._adv()
            return Token(TT_EQ,"=",start_line,start_col)

        if ch=="!" and self._peek(1)=="{":
            self._adv()
            self._adv()
            name_line=self.line
            name_col=self.col
            j=self.i
            while True:
                c=self._peek()
                if c=="" or c=="\n":
                    raise LexError("Unterminated constant reference",start_line,start_col)
                if c=="}":
                    break
                self._adv()
            name=self.src[j:self.i]
            if not _ident_re.fullmatch(name):
                raise LexError(f"Invalid constant name '{name}'",name_line,name_col)
            self._adv()
            return Token(TT_CONSTREF,name,start_line,start_col)

        raise LexError(f"Unexpected character '{ch}'",start_line,start_col)
