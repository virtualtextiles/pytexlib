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
import os
from .yarn import Yarn
from .yarngroup import YarnGroup
from .fiber import Fiber
import colorsys
import itertools

import vedo


class Textile:
    yarn_groups = []

    def __init__(self, yarn_groups=None, name="textile"):

        if yarn_groups == None:
            yarn_groups = []

        self.yarn_groups: list[YarnGroup] = yarn_groups
        self.name: str = name

    def __repr__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}"'

    def __str__(self):
        cls = self.__class__.__name__
        return f'{cls} "{self.name}" with {len(self)} yarn groups'

    def __getitem__(self, arg):
        return self.yarn_groups[arg]

    def __len__(self):
        return len(self.yarn_groups)

    def add_yarn_group(self, yarn_group):
        self.yarn_groups.append(yarn_group)

    def to_reco(self, reco_export_directory=None):
        """Writes the textile data as RECO file to a given directory.
        If no directory is specified, a directory with the name of the textile is created in the current working directory.

        Args:
            directory (_type_, optional): _description_. Defaults to None.
        """

        if reco_export_directory == None:
            reco_export_directory = os.path.join(os.path.curdir, f"{self.name}")

        if not os.path.isdir(reco_export_directory):
            os.mkdir(reco_export_directory)

        # write all fiber files and collect all fibernames
        all_fiber_file_names = []

        for yg_idx, yarn_group in enumerate(self.yarn_groups):
            for y_idx, yarn in enumerate(yarn_group.yarns):
                for f_idx, fiber in enumerate(yarn.fibers):

                    fiber_file_name = (
                        f"{self.name}_{yarn_group.name}_{yarn.name}_{fiber.name}_({yg_idx}{yg_idx}{f_idx})"
                    )
                    fiber_file_uri = os.path.join(
                        reco_export_directory, fiber_file_name
                    )

                    fiber.write_reco_file(
                        fiber_file_uri
                    )  # here the fiber files are created
                    all_fiber_file_names.append(fiber_file_name)

        # master file operation

        nr_of_yarn_files = len(all_fiber_file_names)
        reco_master_file_name = f"{self.name}.csv"
        reco_master_file_uri = os.path.join(
            reco_export_directory, reco_master_file_name
        )

        with open(reco_master_file_uri, "w") as file:
            file.write("Version 2.4.Muster;  RECO Master File\n")
            file.write("1;" + str(1) + ";" + str(1) + "\n")
            file.write(f"{nr_of_yarn_files}\n")
            for file_idx, file_name in enumerate(all_fiber_file_names):
                file.write(file_name + "\n")

    def as_vedo_assembly(self):
        return vedo.Assembly([yg.as_vedo_assembly() for yg in self.yarn_groups])

    def make_resolution_assembly(self):
        
        a=vedo.Assembly([yg.make_resolution_assembly() for yg in self.yarn_groups])

        segment_distances=self.segment_distances

        min_segment_distance=min(segment_distances)
        max_segment_distance=max(segment_distances)

        scalarbar_made=False
        scalarbar=None

        for yg_assembly in a.objects:
            for y_assembly in yg_assembly.objects:
                for f_idx,f in enumerate(y_assembly.objects):
                    f.lw(2)
                    f.cmap("rainbow",vmin=min_segment_distance,vmax=max_segment_distance)
                    
                    if not scalarbar_made:
                        scalarbar=f.add_scalarbar("Segment Length")
                        scalarbar_made=True
        return a,scalarbar
    
    def normalize_scale(self):
        # TODO!!
        pass

    def print_structure(self, level=3):

        print(f"{self.name} ({len(self.yarn_groups)})")

        if level > 0:
            for yg_idx, yarn_group in enumerate(self.yarn_groups):
                print(
                    f"\t\t└Yarn Group {yg_idx} '{yarn_group.name}' ({len(yarn_group)})"
                )
                if level > 1:
                    for y_idx, yarn in enumerate(yarn_group.yarns):
                        print(
                            f"\t\t\t└Yarn {yg_idx}.{y_idx} '{yarn.name}' ({len(yarn)})"
                        )
                        if level > 2:
                            for f_idx, fibre in enumerate(yarn.fibers):
                                print(
                                    f"\t\t\t\t└Fibre {yg_idx}.{y_idx}.{f_idx} {fibre.name} ({fibre.nr_of_points})"
                                )

    @property
    def nr_of_fibers(self):
        nr_of_fibers = 0
        for yarn_group in self.yarn_groups:
            for yarn in yarn_group:
                nr_of_fibers += len(yarn)
        return nr_of_fibers

    @property
    def nr_of_yarns(self):
        nr_of_yarns = 0
        for yarn_group in self.yarn_groups:
            nr_of_yarns += len(yarn_group)
        return nr_of_yarns

    @property
    def yarns(self):
        all_yarns_unflattened = [[y for y in yg.yarns] for yg in self.yarn_groups]
        all_yarns_flattened = list(itertools.chain.from_iterable(all_yarns_unflattened))
        return all_yarns_flattened

    @property
    def fibers(self):
        all_fibers_unflattened = [[[f for f in y.fibers] for y in yg.yarns] for yg in self.yarn_groups]
        all_fibers_flattened = list(
            itertools.chain.from_iterable(all_fibers_unflattened)
        )
        return all_fibers_flattened

    @property
    def segment_distances(self):
        '''
        flat array with segment distances of all fibers
        useful for getting min/max values etc
        '''
        segment_distances=[]
        for yg_idx, yarn_group in enumerate(self.yarn_groups):
            for ya_idx, yarn in enumerate(yarn_group.yarns):
                for f_idx, fiber in enumerate(yarn.fibers):
                    segment_distances.append(fiber.segment_distances)
        segment_distances=np.concat(segment_distances)
        return segment_distances

    def colormap_yarn_groups(self):
        '''
        TODO: Make matplotlib colormaps available for this
        '''
        hue_steps = np.linspace(0, 1, len(self.yarn_groups))
        for yg_idx, yarn_group in enumerate(self.yarn_groups):
            for ya_idx, yarn in enumerate(yarn_group.yarns):
                s_steps = np.linspace(.2, .8, len(yarn.fibers))
                for f_idx, fiber in enumerate(yarn.fibers):
                    h = hue_steps[yg_idx]
                    s = 1
                    v = 1
                    r, g, b = [int(v * 255) for v in colorsys.hsv_to_rgb(h, s, v)]
                    fiber.red = r
                    fiber.green = g
                    fiber.blue = b

    def colormap_yarns(self):
        '''
        TODO: Make matplotlib colormaps available for this
        '''
        all_yarns=self.yarns
        hue_steps = np.linspace(0, 1, len(all_yarns))

        for ya_idx, yarn in enumerate(all_yarns):
            s_steps = np.linspace(.2, .8, len(yarn.fibers))
            for f_idx, fiber in enumerate(yarn.fibers):
                h = hue_steps[ya_idx]
                s = s_steps[f_idx]
                v = 1
                r, g, b = [int(v * 255) for v in colorsys.hsv_to_rgb(h, s, v)]
                fiber.red = r
                fiber.green = g
                fiber.blue = b
                
    def colormap_fibers(self):
        '''
        TODO: Make matplotlib colormaps available for this
        '''
        all_yarns=self.yarns   
        for ya_idx, yarn in enumerate(all_yarns):
            hue_steps = np.linspace(0, 1, len(yarn.fibers))
            for f_idx, fiber in enumerate(yarn.fibers):
                h = hue_steps[f_idx]
                s = 1
                v = 1
                r, g, b = [int(v * 255) for v in colorsys.hsv_to_rgb(h, s, v)]
                fiber.red = r
                fiber.green = g
                fiber.blue = b

    # def plot(self,backend="vedo"): #TODO
    #     '''
    #     backends=["vedo","matplotlib"]
    #     '''
    #     if backend=="Vedo":
    #         vplt_textile=vedo.Plotter()
    #         vplt_textile.add(self.as_vedo_assembly())
            
    #         vplt_textile.show().interactive().close()

        
        

