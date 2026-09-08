from .yarn import Yarn
import vedo

class YarnGroup:
    yarns=[]
    
    def __init__(self,yarns=None,name="yarngroup"):
        
        if yarns==None:
            yarns=[]
        
        self.yarns:list[Yarn]=yarns
        self.fiberfilenames=[]
        self.name:str=name
        
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}"'

    def __str__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}" with {len(self)} yarn groups'
    
    def __getitem__(self, arg):
        return self.yarns[arg]
    
    def __len__(self):
        return len(self.yarns)

    def add_yarn(self, yarn:Yarn):
        self.yarns.append(yarn)
        
    def as_vedo_assembly(self):
            return vedo.Assembly([y.as_vedo_assembly() for y in self.yarns])
    
    def make_resolution_assembly(self):
            return vedo.Assembly([y.make_resolution_assembly() for y in self.yarns])