class RuntimeErrorPPL(Exception): pass
class Environment:
    def __init__(self,parent=None): self.values={}; self.parent=parent
    def define(self,n,v): self.values[n]=v
    def get(self,n):
        if n in self.values: return self.values[n]
        if self.parent: return self.parent.get(n)
        raise RuntimeErrorPPL(f"Undefined variable '{n}'.")
    def assign(self,n,v):
        if n in self.values: self.values[n]=v; return
        if self.parent: self.parent.assign(n,v); return
        raise RuntimeErrorPPL(f"Undefined variable '{n}'.")
