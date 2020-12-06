# Fiber Library
# For storing textile fiber information 
# and writting ReCo 2.0 File Formats for Textiles. 
# ReCo Files can be imported and viewed with the Free TexMind Textiles Viewer (www.texmind.com)
# or can be used as coordinate files 
# 
# Copyright (c) <2020> <Yordan Kyosev>
# This file is distributed under MIT License

import math
import numpy as np

class fiber:
    diameter=1
    xyz=[]
    nrpoints=0
    E=0
    fric=0.3
    red=12
    green=255
    blue=23
    name="fib1"
    
    def __init__(self):
        self.xyz = []
        self.diameter=1
        self.xyz=[]
        self.nrpoints=0
        self.E=0
        self.fric=0.3
        self.red=12
        self.green=255
        self.blue=23
        self.name="fib1"
    def setcolour(self,red_,green_,blue_):
        self.red=red_
        self.green=green_
        self.blue=blue_
        
    def create(self, d, x,y,z):
        self.xyz=np.zeros((len(x), 3),dtype=float)
        for i in range (0,len(x)):
            self.xyz[i]=[x[i],y[i],z[i]]
            self.diameter=d
            
    def append_point(self,x,y,z):
        if (len(self.xyz)<1):
            self.xyz=np.array([[x,y,z]])
        else:
            self.xyz=np.append(self.xyz, np.array([[x, y, z]]),axis=0)
            
    def write_file(self):
        file = open(self.name,"w")
        nrPoints=len(self.xyz[:,0])
        file.write("Garn-Format Ver. 2.0 RECO-CSV\n")
        file.write("TotalFibers\n")
        file.write("1\n")
        file.write("Fiber\n")
        file.write("1;" + str(self.diameter) + ";0;0;0\n")
        file.write(str(self.red) + ";" + str(self.green) + ";" + str(self.blue) + ";\n")
        file.write(str(nrPoints) + "\n")
        for i in range(nrPoints):
            file.write(str(self.xyz[i,0]) + ";" + str(self.xyz[i,1]) + ";"+ str(self.xyz[i,2]) + ";\n")
        file.close()


 