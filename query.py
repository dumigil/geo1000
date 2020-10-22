# GEO1000 - Assignment 4
# Authors: Michiel de Jong
# Studentnumbers: 4376978

from reader import read
from geometry import Rectangle, Circle, Point
from os.path import basename


def parse(geom_str):
    """Parse a string into a shape object (Point, Circle, or Rectangle)

    Formats that can be given:
    p <px> <py>
    c <cx> <cy> <r>
    r <llx> <lly> <urx> <ury>
    
    Returns - Point, Circle, or Rectangle
    """
    geom_str = geom_str.split(" ")
    if geom_str[0] == 'p':
        geom_str.pop(0)
        p_list = []
        for l in geom_str:
            l = float(l)
            p_list.append(l)
        pt = Point(p_list[0],p_list[1])
        return pt
    elif geom_str[0] == 'c':
        geom_str.pop(0)
        c_list = []
        for l in geom_str:
            l = float(l)
            c_list.append(l)
        crcl = Circle(Point(c_list[0],c_list[1]),c_list[2])
        return crcl
    elif geom_str[0] == 'r':
        geom_str.pop(0)
        r_list = []
        for l in geom_str:
            l = float(l)
            r_list.append(l)
        rctgl = Rectangle(Point(r_list[0],r_list[1]),Point(r_list[2],r_list[3]))
        return rctgl


def print_statistics(result):
    """Prints statistics for the resulting list of Points of a query
    
    * Number of points overlapping (i.e. number of points in the list)
    * The leftmost point and its identity given by the id function
    * The rightmost point and its identity given by the id function
    
    Returns - None
    """
    header = """
+--------------+
+ Result       +
+--------------+"""
    print(header)
    if len(result) > 0:
        print(str(len(result)) + " point(s)")
        point_left = result[0]
        point_right = result[0]
        for point in result: 
            if point.x < point_left.x or (point.x == point_left.x and point.y < point_left.y):
                point_left = point
            if point.y > point_right.y or (point.x == point_right.x and point.y > point_right.y):
                point_right = point
        print("The leftmost: {} id {}".format(point_left, id(point_left)))
        print("The rightmost: {} id {}".format(point_right, id(point_right)))
    else:
        print("There are no overlapping points")


def print_help():
    """Prints a help message to the user, what can be done with the program.
    """
    helptxt = """
Commands available:
-------------------
General:
    help
    quit

Reading points in a structure, defining how many strips should be used:
    open <filenm> into <number_of_strips>

Querying:
    with a point:     p <px> <py>
    with a circle:    c <cx> <cy> <radius>
    with a rectangle: r <llx> <lly> <urx> <ury>"""
    print(helptxt)

# =============================================================================
# Below are some commands that you may use to test your codes:
# open points2.txt into 5
# p 5.0 5.0
# c 10.0 10.0 1.0
# r 2.0 2.0 8.0 4.0
# =============================================================================
def main():
    """The main function of this program.
    """
    structure = None
    print("Welcome to {0}.".format(basename(__file__)))
    print("=" * 76)
    print_help()
    while True:
        in_str = input("your command>>>\n").lower()
        if in_str.startswith("quit"):
            print("Bye, bye.")
            return
        elif in_str.startswith("help"):
            print_help()
        elif in_str.startswith("open"):
            filenm, nstrips = in_str.replace("open ", "").split(" into ")
            structure = read(filenm, int(nstrips))
            structure.print_strip_statistics()
        elif in_str.startswith("p") or in_str.startswith("c") or in_str.startswith("r"):
            if structure is None:
                print("No points read yet, open a file first!")
            else:
                print_statistics(structure.query(parse(in_str)))

if __name__ == "__main__":
    main()

