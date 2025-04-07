### shapes.py
# Shapes library for tangram and further references
# A shape is defined by its edge point, its center and vectors

import numpy as np
import pygame
import math
from cfg import COLORS, VECTOR_LENGTH

VECTOR_LENGTH = 15

def get_trgl_cog(size):
	return np.round(2*size/3, 3)

TRGL_LNGTH_SML = 73.7
TRGL_SML_COG = get_trgl_cog(TRGL_LNGTH_SML)

TRGL_LNGTH_MID = 104.5
TRGL_MID_COG = get_trgl_cog(TRGL_LNGTH_MID)

TRGL_LNGTH_LRG = 147.5
TRGL_LRG_COG = get_trgl_cog(TRGL_LNGTH_LRG)

SQR_SIZE = 74 

def init_shapes():
	cfg.SHAPES = {
		"triangle_small": {
			"points": [(TRGL_LNGTH_SML, TRGL_LNGTH_SML), (TRGL_LNGTH_SML, 0), (0, TRGL_LNGTH_SML)],
			"vectors": [(-(VECTOR_LENGTH - TRGL_SML_COG)*np.sin(np.pi/4), (VECTOR_LENGTH - TRGL_SML_COG)*np.cos(np.pi/4)),
			((VECTOR_LENGTH - TRGL_SML_COG)*np.cos(np.pi/4), (VECTOR_LENGTH - TRGL_SML_COG)*np.sin(np.pi/4))],  # Example vectors for the triangle
			"count": 2
		},
		"triangle_mid": {
			"points": [(TRGL_LNGTH_MID, TRGL_LNGTH_MID), (TRGL_LNGTH_MID, 0), (0, TRGL_LNGTH_MID)],
			"vectors": [(-(VECTOR_LENGTH - TRGL_MID_COG)*np.sin(np.pi/4), (VECTOR_LENGTH - TRGL_MID_COG)*np.cos(np.pi/4)),
			((VECTOR_LENGTH - TRGL_MID_COG)*np.cos(np.pi/4), (VECTOR_LENGTH - TRGL_MID_COG)*np.sin(np.pi/4))],  # Example vectors for the triangle
			"count": 1
		},
		"triangle_large": {
			"points": [(TRGL_LNGTH_LRG, TRGL_LNGTH_LRG), (TRGL_LNGTH_LRG, 0), (0, TRGL_LNGTH_LRG)],
			"vectors": [(-(VECTOR_LENGTH - TRGL_LRG_COG)*np.sin(np.pi/4), (VECTOR_LENGTH - TRGL_LRG_COG)*np.cos(np.pi/4)),
			((VECTOR_LENGTH - TRGL_LRG_COG)*np.cos(np.pi/4), (VECTOR_LENGTH - TRGL_LRG_COG)*np.sin(np.pi/4))],  # Example vectors for the triangle
			"count": 2
		},
		"square": {
			"points": [(0, 0), (SQR_SIZE , 0), (SQR_SIZE , SQR_SIZE), (0, SQR_SIZE)],
			"vectors": [(VECTOR_LENGTH, 0), (0, -VECTOR_LENGTH)],  # Example vectors for the square
			"count": 1
		},
		"parallelogram": {
			"points": [(0 ,52.05), (52.6, 0), (52.6, 100), (0, 152.05)],
			"vectors": [(VECTOR_LENGTH, 0), (0, -VECTOR_LENGTH)],  # Example vectors for the parallelogram
			"count": 1
		}
	}



class Shape:
    def __init__(self, shape_type, center, angle=0):
        self.shape_type = shape_type
        self.center = center
        self.angle = angle
        self.color = COLORS[len(pieces) % len(COLORS)]

    def get_global_points(self):
        points = SHAPES[self.shape_type]["points"]
        rotated_points = self.rotate(points, self.angle)
        cog = self.get_center_of_gravity(rotated_points)
        return [(x - cog[0] + self.center[0], y - cog[1] + self.center[1]) for x, y in rotated_points]

    def rotate(self, points, angle):
        angle_rad = math.radians(angle)
        return [(x * math.cos(angle_rad) - y * math.sin(angle_rad), x * math.sin(angle_rad) + y * math.cos(angle_rad)) for x, y in points]

    def get_center_of_gravity(self, shape_points):
        x_coords = [p[0] for p in shape_points]
        y_coords = [p[1] for p in shape_points]
        return (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

def extract_counts(shapes):
    counts = {}
    for shape in shapes.keys():
        counts[shape] = shapes[shape]["count"]
    return counts


