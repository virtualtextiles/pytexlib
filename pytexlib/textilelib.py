# Textiles Library
# For storing textile fiber information
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
from yarnlib import *
from copy import deepcopy

# for 3D install vtk and pyvista

import pyvista as pv


class textile:
    yarns = []
    name = "textile"
    fibfinames = []

    def __init__(self):
        self.yarns = []
        self.name = "textile"
        self.fibfinames = []

    def add_yarn(self, yarn):
        group = []
        self.yarns.append(deepcopy(yarn))

    def write_file(self, filename):
        # write all fiber files and collect all fibernames
        nryarns = len(self.yarns)
        for i in range(0, nryarns):
            self.yarns[i].name = self.name + \
                str(self.yarns[i].groupID) + "_" + str(i)
            print(self.yarns[i].name)
            self.yarns[i].write_file()  # here the fiber names are created

            for ifib in range(0, len(self.yarns[i].fiberfilenames)):
                self.fibfinames.append(self.yarns[i].fiberfilenames[ifib])

        # master file operation
        file = open(filename, "w")
        file.write("Version 2.4.Muster;  RECO Master File\n")
        file.write("1;" + str(1) + ";" + str(1) + "\n")

        NrYarnFiles = len(self.fibfinames)
        file.write(str(NrYarnFiles)+"\n")
        for i in range(len(self.fibfinames)):
            file.write(self.fibfinames[i] + "\n")

        file.close

    def plot(self):
        # write all fiber files and collect all fibernames
        nryarns = len(self.yarns)
        for i in range(0, nryarns):
            for ifib in range(0, len(self.yarns[i].fiberfilenames)):
                poly = pv.PolyData()
                poly.points = self.yarns[i].fibers[i].xyz
                the_cell = np.arange(0, len(poly.points), dtype=np.int_)
                the_cell = np.insert(the_cell, 0, len(poly.points))
                poly.lines = the_cell

                # polyline = polyline_from_points(points)
                poly["scalars"] = np.arange(poly.n_points)
                tube = poly.tube(radius=0.1)
                tube.plot(smooth_shading=True)