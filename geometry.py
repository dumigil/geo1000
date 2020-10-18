# GEO1000 - Assignment 4
# Authors: Michiel de Jong
# Studentnumbers: 4376978

import math

# __all__ leaves out _test method and only makes
# the classes available for "from geometry import *":
__all__ = ["Point", "Circle", "Rectangle"] 


class Point(object):

    def __init__(self, x, y):
        """Constructor. 
        Takes the x and y coordinates to define the Point instance.
        """
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        """Returns WKT String "POINT (x y)".
        """
        wkt = "POINT (%s,%s)"%(self.x, self.y)
        return wkt

    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        returns - True / False
        """
        if isinstance(other, Point):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        elif isinstance(other, Circle):
            if self.distance(other.center) <= other.radius:
                print('yes')
                return True
            else:
                return False 
        elif isinstance(other, Rectangle):
            if self.x >= other.ll.x and self.x <= other.ur.x and self.y >= other.ll.y and self.y <= other.ur.y:
                print('yes')
                return True
            else:
                return False 

    def distance(self, other):
        """Returns cartesian distance between self and other Point
        """
        assert isinstance(other, Point)
        dist = math.sqrt(abs(self.x - other.x)**2 + abs(self.y - other.y)**2)
        return dist


class Circle(object):

    def __init__(self, center, radius):
        """Constructor. 
        Takes the center point and radius defining the Circle.
        """
        assert radius > 0
        assert isinstance(center, Point)
        self.center = center
        self.radius = float(radius)

    def __str__(self):
        """Returns WKT str, discretizing the boundary of the circle 
        into straight line segments
        """
        N = 400
        step = 2 * math.pi / N
        pts = []
        for i in range(N):
            pts.append(Point(self.center.x + math.cos(i * step) * self.radius, 
                             self.center.y + math.sin(i * step) * self.radius))
        pts.append(pts[0])
        coordinates = ["{0} {1}".format(pt.x, pt.y) for pt in pts]
        coordinates = ", ".join(coordinates)
        return "POLYGON (({0}))".format(coordinates)

    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        Returns - True / False
        """
        if isinstance(other, Point):
            if other.intersects(self) == True:
                return True
            else:
                return False
        elif isinstance(other, Circle):
            if self.distance(other.center) <= other.radius:
                print('yes')
                return True
            else:
                return False 
        elif isinstance(other, Rectangle):
            if self.x >= other.ll.x and self.x <= other.ur.x and self.y >= other.ll.y and self.y <= other.ur.y:
                print('yes')
                return True
            else:
                return False 


class Rectangle(object):

    def __init__(self, pt_ll, pt_ur):
        """Constructor. 
        Takes the lower left and upper right point defining the Rectangle.
        """
        assert isinstance(pt_ll, Point)
        assert isinstance(pt_ur, Point)
        self.ll = pt_ll
        self.ur = pt_ur
        self.ul = Point(self.ll.x, (self.ll.y + self.height()))
        self.lr = Point(self.ur.x, (self.ur.y - self.height()))

    def __str__(self):
        """Returns WKT String "POLYGON ((x0 y0, x1 y1, ..., x0 y0))"
        """
        wkt  = "POLYGON ((%s %s,%s %s,%s %s,%s %s,%s %s))"%(self.ll.x, self.ll.y,self.lr.x,self.lr.y,self.ur.x,self.ur.y,self.ul.x,self.ul.y,self.ll.x,self.ll.y)
        return wkt

    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        Returns - True / False
        """
        
        

    def width(self):
        """Returns the width of the Rectangle.
        
        Returns - float
        """
        wide = self.ur.x - self.ll.x
        return wide

    def height(self):
        """Returns the height of the Rectangle.
        
        Returns - float
        """
        high = self.ur.y - self.ll.y
        return high


def _test():
    """Test whether your implementation of all methods works correctly.
    """
    pt0 = Point(0, 0)
    pt1 = Point(0, 0)
    pt2 = Point(10, 10)
    assert pt0.intersects(pt1)
    assert pt1.intersects(pt0)
    assert not pt0.intersects(pt2)
    assert not pt2.intersects(pt0)
    
    c = Circle(Point(-1, -1), 1)
    r = Rectangle(Point(0,0), Point(10,10))
    #print(r.__str__())
    #print(c.__str__())
    assert not c.intersects(r)
    assert pt0.intersects(c)
    assert pt0.intersects(r)
    # Extend this method to be sure that you test all intersects methods!
    # Read Section 16.5 of the book if you have never seen the assert statement


if __name__ == "__main__":
    _test()

