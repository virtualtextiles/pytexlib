# Fiber Library
# For storing textile fiber information
#
# Copyright (c) <2020> <Yordan Kyosev>
# This file is distributed under MIT License

import math
import numpy as np
from matplotlib import pyplot as plt
import vedo


class Fiber:
    diameter: float = 1
    xyz: np.ndarray = np.array([])
    _xyz_original: np.ndarray = np.array([])
    
    def __init__(
        self,
        xyz=None,
        diameter: float = 1.0,
        E: float = 0,
        friction: float = 0,
        color=None,
        name:str="Fiber",
    ):
        if xyz==None:
            xyz=np.array([])
        
        if color==None:
            color=[12,60,199]
        
        self._xyz_initial = xyz.copy()
        self.xyz = xyz
        self.diameter = diameter
        self.E = E
        self.friction = friction
        self.red, self.green, self.blue = color
        self.name = name

    def __str__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}"'

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}" with {self.nr_of_points} Points'

    def __getitem__(self, arg):
        return self.xyz[arg, :]

    def set_color(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def nr_of_points(self):
        return self.xyz.shape[0]

    # def add_points_from_separate_vectors(self, d, x, y, z):
    #     '''
    #     TODO Move this somwhere sensible
    #     '''
    #     self.xyz = np.hstack([x,y,z])
    #     self.diameter = d
        

    def append_point(self, x, y, z):
        if len(self.xyz) < 1:
            self.xyz = np.array([[x, y, z]])
        else:
            self.xyz = np.append(self.xyz, np.array([[x, y, z]]), axis=0)

    def write_reco_file(self,filename=None):
        if filename==None:
            filename=self.name
            
        with open(filename, "w") as file:   
            file.write("Garn-Format Ver. 2.0 RECO-CSV\n")
            file.write("TotalFibers\n")
            file.write("1\n")
            file.write("Fiber\n")
            file.write("1;" + str(self.diameter) + ";0;0;0\n")
            file.write(str(self.red) + ";" + str(self.green) + ";" + str(self.blue) + ";\n")
            file.write(f"{self.nr_of_points}" + "\n")
            for pt_idx in range(self.nr_of_points):
                file.write(
                    str(self.xyz[pt_idx, 0])
                    + ";"
                    + str(self.xyz[pt_idx, 1])
                    + ";"
                    + str(self.xyz[pt_idx, 2])
                    + ";\n"
                )
            file.close()

    def load_CSV(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            for i in range(9, len(lines)):
                xyzs = lines[i].split(";")
                x = float(xyzs[0].replace(",", "."))
                y = float(xyzs[1].replace(",", "."))
                z = float(xyzs[2].replace(",", "."))
                self.append_point(x, y, z)

    def get_xyz(self):
        """returns x, y, and z as separate vectors for ploting or so
        Returns:
            _type_: _description_
        """
        return [self.xyz[:, i] for i in range(3)]

    def equal_interpolation(self,length):
        '''
        Pass a length with which the points are resampled along the line.
        '''
        
        
    
    
    def plot_3d(self):
        fig = plt.figure(figsize=(10, 10), frameon=True, dpi=150)
        ax = fig.add_subplot(111, projection="3d")
        x, y, z = self.get_xyz()
        ax.plot(
            x,
            y,
            z,
            "k-",
            label="Fiber",
        )
        plt.show(block=False)

    def as_vedo_tube(self,cap=True,res=12):

        yarn_tube = vedo.Tube(points=self.xyz, r=self.diameter, cap=cap, res=res, alpha=1.0)
        yarn_tube.c((self.red, self.green, self.blue))

        yarn_tube.name = self.name
        return yarn_tube
    
    def make_resolution_assembly(self):
        yarn_line = vedo.Line(self.xyz)
        yarn_line.c((self.red, self.green, self.blue))
        yarn_points= vedo.Points(self.xyz)
        
        return vedo.Assembly(yarn_line,yarn_points)
    
    