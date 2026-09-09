# Fiber Library
# For storing textile fiber information
#
# Copyright (c) <2020> <Yordan Kyosev>
# This file is distributed under MIT License

import math
import numpy as np
from matplotlib import pyplot as plt
import vedo

import numpy as np
from scipy.interpolate import interp1d,splprep, splev

class Fiber:    
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
        
        # self._xyz_initial = np.copy(xyz)
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

    @property
    def point_distances(self):
        distances=np.sqrt(np.sum(np.diff(self.xyz,axis=0)**2,axis=1))
        return distances
    
    @property
    def segment_distances(self):
        '''calculate the distances of all polyline sections        
        '''
        return np.sqrt(np.sum(np.diff(self.xyz, axis=0)**2, axis=1))

    @property
    def length(self):
        '''length of the whole polyline
        '''
        return np.sum(self.segment_distances)
    
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

    def equal_spaced_interpolation(self,nr_of_points):
        '''
        Resample the polyline equally with a given number of points
        '''
        
        cumulative_dist= np.insert(np.cumsum(self.segment_distances), 0, 0)
        f_interp = interp1d(cumulative_dist, self.xyz, axis=0, kind='linear')
        # # Generate evenly spaced target distances
        total_length = cumulative_dist[-1]
        uniform_dist = np.linspace(0, total_length, nr_of_points)
        resampled_points = f_interp(uniform_dist)
        self.xyz=resampled_points
        
    # def reset_xyz_data(self):
    #     '''
    #     Reset XYZ to original input
    #     '''
    #     self.xyz=self._xyz_initial.copy() 
   
    
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
    
    def make_resolution_assembly(self,show_points=False):

        
        # Get pairs of consecutive points
        pairs = np.stack((self.xyz[:-1], self.xyz[1:]), axis=1)
        first_elements = pairs[:,0]
        second_elements = pairs[:,1]
        yarn_line_segments=vedo.Lines(first_elements,second_elements)

        yarn_line_segments.celldata["distance"] = self.segment_distances
        yarn_line_segments.cmap("rainbow")        
        return yarn_line_segments
    
    def resample_polyline_by_count(self, num_points):
        '''
        linear interpolation, with a given amount of points
        '''
        points=self.xyz
        # Compute segment lengths and cumulative arc-length
        seg_lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
        arc_length = np.concatenate([[0], np.cumsum(seg_lengths)])
        # Remove duplicate arc-lengths (and corresponding points)
        unique_arc, unique_idx = np.unique(arc_length, return_index=True)
        unique_points = points[unique_idx]
        # Build interpolators
        interp_x = interp1d(unique_arc, unique_points[:,0])
        interp_y = interp1d(unique_arc, unique_points[:,1])
        interp_z = interp1d(unique_arc, unique_points[:,2])
        # Generate new arc-lengths
        new_arc = np.linspace(0, unique_arc[-1], num_points)
        # Evaluate interpolators
        resampled = np.stack([interp_x(new_arc), interp_y(new_arc), interp_z(new_arc)], axis=-1)
        self.xyz=resampled

    
    def resample_polyline_by_spacing(self, spacing):
        '''
        linear interpolation with a given spacing
        '''
        
        points=self.xyz
        seg_lengths = np.linalg.norm(np.diff(points, axis=0), axis=1)
        arc_length = np.concatenate([[0], np.cumsum(seg_lengths)])
        unique_arc, unique_idx = np.unique(arc_length, return_index=True)
        unique_points = points[unique_idx]
        interp_x = interp1d(unique_arc, unique_points[:,0])
        interp_y = interp1d(unique_arc, unique_points[:,1])
        interp_z = interp1d(unique_arc, unique_points[:,2])
        # The fix: use np.arange to guarantee minimum spacing
        new_arc = np.arange(0, unique_arc[-1] + 1e-10, spacing)
        resampled = np.stack([interp_x(new_arc), interp_y(new_arc), interp_z(new_arc)], axis=-1)
        self.xyz=resampled
    
    def fit_b_spline(self,order=3,smoothing=0,n_points=50):
        '''
        b-spline interpolation with a given number of points
        '''
        tck, u = splprep(self.xyz.T, s=smoothing, k=order)
        # 3. Evaluate the spline at fine intervals
        u_fine = np.linspace(0, 1, n_points)
        x_spline, y_spline, z_spline = splev(u_fine, tck)
        # print(np.hstack([x_spline,y_spline,z_spline]))
        xyz_new=np.array([*zip(x_spline, y_spline, z_spline)])
        self.xyz=xyz_new