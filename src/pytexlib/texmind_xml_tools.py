from .structures import Fiber, Yarn, Textile, YarnGroup
import xml.etree.ElementTree as ET
import numpy as np


def from_xml(file_path):
    """
    Parses a textile structure XML file and returns a list of strands,
    each with an 'xyz' attribute containing a NumPy array of fiber coordinates.

    Args:
        file_path (str): Path to the tubu.xml file.

    Returns:

    """

    tree = ET.parse(file_path)

    root = tree.getroot()
    yarn_groups_xml = root.findall("YarnGroup")

    T = Textile()
    T.name = str(root.find("mName").get("value"))

    for yg_idx, yarn_group in enumerate(yarn_groups_xml):

        YG = YarnGroup()
        yarn_group_name=str(yarn_group.find("mName").get("value"))
        YG.name=yarn_group_name
        yarns_xml = yarn_group.findall("Yarn")
        
        for y_idx, yarn in enumerate(yarns_xml):

            Y = Yarn()
            yarn_name = str(yarn.find("mName").get("value"))
            Y.name = yarn_name
            fibres_xml = yarn.findall("Fibre")

            for f_idx, fibre in enumerate(fibres_xml):

                fi = Fiber()
                fiber_name = str(fibre.find("mName").get("value"))
                fi.name = fiber_name
                coords = []

                for point in fibre.findall("Point"):
                    x = float(point.find("mX").get("value"))
                    y = float(point.find("mY").get("value"))
                    z = float(point.find("mZ").get("value"))
                    coords.append([x, y, z])
                    
                diameter = float(fibre.find("mDiameter").get("value"))                
                
                red = float(fibre.find("mRed").get("value"))
                green = float(fibre.find("mGreen").get("value"))
                blue = float(fibre.find("mBlue").get("value"))              
                
                
                fi.xyz = np.array(coords)
                fi.diameter = diameter
                fi.set_color(red,green,blue)
                
                Y.add_fiber(fi)
                
            YG.add_yarn(Y)
        T.add_yarn_group(YG)
    return T


def print_xml_yarn_structure(file_path, level=0):
    tree = ET.parse(file_path)
    root = tree.getroot()
    yarn_groups = root.findall("YarnGroup")
    name = root.find("mName").get("value")
    print(f"{name}")
    if level == 0:
        level = np.inf
    if level > 0:
        print(f"\t└Yarn Groups({len(yarn_groups)})")
        if level > 1:
            for yg_idx, yarn_group in enumerate(yarn_groups):
                print(f"\t\t└Yarn Group {yg_idx} ({len(yarn_group)})")
                if level > 2:
                    for y_idx, yarn in enumerate(yarn_group.findall("Yarn")):
                        print(f"\t\t\t└Yarn {yg_idx}.{y_idx} ({len(yarn)})")
                        if level > 3:
                            for f_idx, fibre in enumerate(yarn.findall("Fibre")):
                                print(
                                    f"\t\t\t\t└Fibre {yg_idx}.{y_idx}.{f_idx} ({len(fibre)})"
                                )
