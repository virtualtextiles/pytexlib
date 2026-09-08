# Yarn Library
import math
import numpy as np
from .fiber import Fiber
from copy import deepcopy
import vedo

class Yarn:
    fibers=[]
    fiberfilenames=[]
    name="yarn"
    
    def __init__(self,fibers=None,):
        
        if fibers==None:
            fibers=[]
        
        self.fibers:list[Fiber]=fibers
        self.fiberfilenames=[]
        # properties as "super fiber", can be actually overwritten from fiber
        # self.asfiber=Fiber() #TODO
        self.name="yarn"
    
    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}"'

    def __str__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}" with {len(self.fibers)} Fibers'

    def __getitem__(self, arg):
        return self.fibers[arg]
        
    def __len__(self):
            return len(self.fibers)
                
    def add_fiber(self,fib):
        self.fibers.append(deepcopy(fib))
        
    
    # !!deprecated
    # def write_file(self):
    #     for fiber_idx,fiber in enumerate(self.fibers):
    #         fiber.name=f"{self.name}_{fiber_idx}"
    #         self.fiberfilenames.append(fiber.name)
    #         fiber.write_reco_file()
        
    def as_vedo_assembly(self):
        return vedo.Assembly([f.as_vedo_tube() for f in self.fibers])
    
    def make_resolution_assembly(self):
        return vedo.Assembly([f.make_resolution_assembly() for f in self.fibers])