# Yarn Library
# For storing textile yarn, based on fibers information 
# and writting ReCo 2.0 File Formats for Textiles. 
# ReCo Files can be imported and viewed with the Free TexMind Textiles Viewer (www.texmind.com)
# or can be used as coordinate files 
# 
# Copyright (c) <2020> <Yordan Kyosev>
# This file is distributed under MIT License



import math
import numpy as np
#import fiberlib as f
from fiberlib import *
from copy import deepcopy

class yarn:
    nrfibers=0
    fibers=[]
    groupID=0
    fiberfilenames=[]
    name="yarn"
    
    asfiber=fiber()
    
    
    def __init__(self):
        self.fibers=[]
        self.nrfibers=0
        self.groupID=0   
        self.fiberfilenames=[]
        # properties as "super fiber", can be actually overwritten from fiber
        self.asfiber=fiber()
        self.name="yarn"
        
        
    #def create(self, d, x,y,z):
    #    self.xyz=np.zeros((len(x), 3),dtype=float)
    #    for i in range (0,len(x)):
    #        self.xyz[i]=[x[i],y[i],z[i]]
    #        self.diameter=d
            
    def add_fiber(self,fib):
        self.fibers.append(deepcopy(fib))
        
    def write_file(self):
        nrfibs=len(self.fibers)
        for i in range (0,nrfibs):
            self.fibers[i].name=self.name + str(i)
            self.fiberfilenames.append(self.fibers[i].name)
            #print(self.fibers[i].name)
            self.fibers[i].write_file()
        
