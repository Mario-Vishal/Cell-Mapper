from scipy.spatial import ConvexHull, convex_hull_plot_2d
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from shapely.geometry import Point, Polygon



#this is a custom class used as a data structure to store cell ID and it's corresponding list of coordinates
#this custom datastructure creates polygon objects for the coordinates
#two methods are used here
# 1. Convex Hull to get the vertices of the polygon outer boundary ignoring all the coordinates which are inside
# 2. and Polygon class from scipy library to create polygons and check whether a given point is inside that polygon or not

class PolygonCell():

    def __init__(self,cell_id,coordinates) -> None:
        self.cell_id = cell_id
        self.coordinates = np.array(coordinates,dtype=float)
        
        self.hull = ConvexHull(self.coordinates)
        self.boundaries = self.coordinates[self.hull.vertices]
        self.polygon = Polygon(coordinates)
        print("--------------------------------------------------------------")
        print(f"Polygon Created for Cell ID: {cell_id} | with cordin")
        print(f"Number of Coordinates for cell ID {cell_id} : {len(self.coordinates)}")
        print("---------------------------------------------------------------")
        print()

    #gets the outer boundary of the polygon
    def getBoundaries(self):

        return self.boundaries
    
    #plots the polygon 
    def plot(self):


        plt.plot(self.coordinates[self.hull.vertices,0], self.coordinates[self.hull.vertices,1], 'r-', lw=2)
        plt.plot(self.coordinates[self.hull.vertices[0],0], self.coordinates[self.hull.vertices[0],1], 'ro')
        plt.show()

    #checks whether given input point lies inside the polygon or not
    def in_polygon(self,point):
        
        return Point(point).within(self.polygon)
        
    

