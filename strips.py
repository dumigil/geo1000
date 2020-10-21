# GEO1000 - Assignment 4
# Authors:
# Studentnumbers:

from geometry import Point, Rectangle


class Strip(object):
    def __init__(self, rectangle):
        """Constructor. Inits a Strip instance with a Rectangle describing 
        its shape and an empty points list.
        """
        assert isinstance(rectangle, Rectangle)
        self.rect = rectangle
        self.points = []
        self.ptll = self.rect.ll
        self.ptrr = self.rect.ur

class StripStructure(object):
    def __init__(self, extent, no_strips):
        """Constructor. Inits a StripStructure instance with the correct
        number of Strip instances and makes sure that the domain is 
        correctly divided over the strips.
        """
        assert isinstance(extent, Rectangle)
        self.strips = []
        self.query_strips = []
        self.no_strips = no_strips
        width = extent.width()/no_strips
        x_ll = extent.ll.x
        y_ll = extent.ll.y
        x_ur = x_ll + width 
        y_ur = extent.ur.y
        while no_strips > 0:
            shape = Strip(Rectangle((Point(x_ll,y_ll)), (Point(x_ur,y_ur))))
            self.strips.append(shape)
            x_ll = x_ll + width
            x_ur = x_ur + width
            no_strips = no_strips - 1 



    def find_overlapping_strips(self, shape):
        """Returns a list of strip objects for which their rectangle intersects 
        with the shape given.
        
        Returns - list of Strips
        """
        self.query_strips = []
        for i in self.strips :
            if i.rect.intersects(shape):
                self.query_strips.append(i)
        return self.query_strips

    def query(self, shape):
        """Returns a list of points that overlaps the given shape.
        
        For this it first finds the strips that overlap the shape,
        using the find_overlapping_strips method.

        Then, all points of the selected strips are checked for intersection
        with the query shape.
        
        Returns - list of Points
        """
        lst = self.find_overlapping_strips(shape)
        points_list = []
        for strips in lst:
            for pts in strips.points:
                if pts.intersects(shape):
                    points_list.append(pts)
        return points_list               

                

    def append_point(self, pt):
        """Appends a point object to the list of points of the correct strip
        (i.e. the strip the Point intersects).

        For this it first finds the strips that overlap the point,
        using the find_overlapping_strips method.

        In case multiple strips overlap the point, the point is added
        to the strip with the left most coordinate.
        
        Returns - None
        """

        assert isinstance(pt, Point)
        lst = self.find_overlapping_strips(pt)
        if len(lst) == 1:
            for i in lst:
                i.points.append(pt)
        elif len(lst) > 1:
            lst[0].points.append(pt)

        """strip = self.find_overlapping_strips(pt)[0]
        strip.points.append(pt)"""
        




    def print_strip_statistics(self):
        """Prints:
        * how many strips there are in the structure

        And then, for all the strips in the structure:
        * an id (starting at 1),
        * the number of points in a strip, 
        * the lower left point of a strip and 
        * the upper right point of a strip.
        
        Returns - None
        """
        print(str(self.no_strips) + " strips")
        for strips in self.strips:
            print('#'+ (str(int(self.strips.index(strips)+1))) + " with " + str(len(strips.points)) + " points, ll: " + str(strips.ptll) + ", ur: " + str(strips.ptrr))

    def dumps_strips(self):
        """Dumps the strips of this structure to a str, 
        which (if saved in a text file) can be loaded as 
        delimited text layer in QGIS.
        
        Returns - str
        """
        lines = "strip;wkt\n"
        for i, strip in enumerate(self.strips, start = 1):
            t = "{0};{1}\n".format(i, strip.rect)
            lines += t
        return lines

    def dumps_points(self):
        """Dumps the points of this structure to a str, 
        which (if saved in a text file) can be loaded as 
        delimited text layer in QGIS.
        
        Returns - str
        """
        lines = "strip;wkt\n"
        for i, strip in enumerate(self.strips, start = 1):
            for pt in strip.points:
                t = "{0};{1}\n".format(i, pt)
                lines += t
        return lines



def test():
    bbox = Rectangle(Point(0,0),Point(10,10))
    ss = StripStructure(bbox,5)
    qshape = Rectangle(Point(5,5),Point(15,15))
    ss.query(qshape)
    ss.print_strip_statistics()
    

if __name__ == "__main__":
    test()
