from .ast_nodes import *
from .environment import Environment, RuntimeErrorPPL
class ReturnSignal(Exception):
    def __init__(self,value): self.value=value
class UserFunction:
    def __init__(self,stmt,closure): self.stmt=stmt; self.closure=closure
    def call(self,interp,args):
        if len(args)!=len(self.stmt.params): raise RuntimeErrorPPL(f'Expected {len(self.stmt.params)} arguments but got {len(args)}.')
        env=Environment(self.closure)
        for n,v in zip(self.stmt.params,args): env.define(n,v)
        old=interp.environment; interp.environment=env
        try:
            interp.execute(self.stmt.body)
        except ReturnSignal as r: return r.value
        finally: interp.environment=old
        return None
class Interpreter:
    def __init__(self): self.environment=Environment(); self.outputs=[]; self.steps=0
    def run(self,statements):
        for s in statements: self.execute(s)
        return self.outputs
    def execute(self,s):
        self.steps+=1
        if self.steps>100000: raise RuntimeErrorPPL('Execution limit exceeded.')
        if isinstance(s,VarDeclaration): self.environment.define(s.name,self.evaluate(s.initializer))
        elif isinstance(s,Assignment): self.environment.assign(s.name,self.evaluate(s.value))
        elif isinstance(s,PrintStatement): self.outputs.append(str(self.evaluate(s.expression)))
        elif isinstance(s,ExpressionStatement): self.evaluate(s.expression)
        elif isinstance(s,Block):
            old=self.environment; self.environment=Environment(old)
            try:
                for x in s.statements: self.execute(x)
            finally: self.environment=old
        elif isinstance(s,IfStatement): self._exec_if(s)
        elif isinstance(s,WhileStatement):
            guard=0
            while self._bool(self.evaluate(s.condition)):
                self.execute(s.body); guard+=1
                if guard>10000: raise RuntimeErrorPPL('Loop limit exceeded.')
        elif isinstance(s,FunctionStatement): self.environment.define(s.name,UserFunction(s,self.environment))
        elif isinstance(s,ReturnStatement): raise ReturnSignal(None if s.value is None else self.evaluate(s.value))
    def _exec_if(self,s):
        if self._bool(self.evaluate(s.condition)): self.execute(s.then_branch)
        elif s.else_branch: self.execute(s.else_branch)
    def evaluate(self,e):
        if isinstance(e,Literal): return e.value
        if isinstance(e,Variable): return self.environment.get(e.name)
        if isinstance(e,Unary):
            v=self.evaluate(e.operand)
            if e.operator=='-': self.num(v); return -v
            if e.operator=='!': return not self._bool(v)
        if isinstance(e,Logical):
            l=self._bool(self.evaluate(e.left)); return (l and self._bool(self.evaluate(e.right))) if e.operator=='and' else (l or self._bool(self.evaluate(e.right)))
        if isinstance(e,Binary): return self.binary(self.evaluate(e.left),e.operator,self.evaluate(e.right))
        if isinstance(e,Call):
            f=self.evaluate(e.callee); args=[self.evaluate(a) for a in e.arguments]
            if not hasattr(f,'call'): raise RuntimeErrorPPL('Only functions can be called.')
            return f.call(self,args)
        raise RuntimeErrorPPL('Unknown expression.')
    def binary(self,l,o,r):
        if o=='+':
            if type(l)==type(r) and isinstance(l,(str,int,float)): return l+r
            raise RuntimeErrorPPL('Operands must have matching numeric or string types.')
        if o in ('-','*','/'): self.nums(l,r); return {'-':lambda:l-r,'*':lambda:l*r,'/':lambda:l/r}[o]() if not(o=='/' and r==0) else (_ for _ in ()).throw(RuntimeErrorPPL('Division by zero.'))
        if o in ('>','<','>=','<='): self.nums(l,r); return {'>':l>r,'<':l<r,'>=':l>=r,'<=':l<=r}[o]
        if o=='==': return type(l)==type(r) and l==r
        if o=='!=': return not(type(l)==type(r) and l==r)
        raise RuntimeErrorPPL(f'Unsupported operator {o}.')
    def _bool(self,v):
        if not isinstance(v,bool): raise RuntimeErrorPPL('Condition must be Boolean.')
        return v
    def num(self,v):
        if isinstance(v,bool) or not isinstance(v,(int,float)): raise RuntimeErrorPPL('Expected a number.')
    def nums(self,a,b): self.num(a); self.num(b)
