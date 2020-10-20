# GEO1000 - Assignment 4
# Authors:
# Studentnumbers:

from geometry import Point, Rectangle, Circle
from strips import StripStructure


def read(file_nm, no_strips):
    """Reads a file with on the first uncommented line a bbox 
    (4 numbers separated by a space) and subsequently 0 or more lines with 
    points (2 numbers separated by a space) into a Strip Structure.
    
    If no valid box is found in the input file, it returns None.
    Otherwise a StripStructure with 0 or more points is returned.
    
    Returns - None or a StripStructure instance
    """
    uncomlines = []
    with open(file_nm, "r") as fh:
        ln = fh.readlines()
        for l in ln:
            l = l.rstrip()
            if l[0] != "#":
                l_list = l.split()
                l_map = map(float, l_list)
                uncomlines.append(list(l_map))
        if len(uncomlines[0]) == 4:
            bbox = Rectangle(Point(uncomlines[0][0],uncomlines[0][1]),Point(uncomlines[0][2],uncomlines[0][3]))
            ss = StripStructure(bbox, no_strips)
            for pt in uncomlines[1:]:
                pt = Point(pt[0],pt[1])
                ss.append_point(pt)
            print(bbox)
            print(ss.print_strip_statistics())


def dump(structure, strip_file_nm="strips.wkt", point_file_nm="points.wkt"):
    """Dump the contents of a strip structure to 2 files that can be opened
    with QGIS.
    
    Returns - None
    """
    with open(strip_file_nm, "w") as fh:
        fh.write(structure.dump_strips())
    with open(point_file_nm, "w") as fh:
        fh.write(structure.dump_points())

def test():
    read("points2.txt",5)

if __name__ == "__main__":
    test()