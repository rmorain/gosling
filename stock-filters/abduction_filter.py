import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
import os

import utilityFunctions as utilityFunctions

inputs = (
	("Story Visualization", "label"),
	("Material", alphaMaterials.Cobblestone), # the material we want to use to build the mass of the structures
	("Creator: BB", "label"),
	)

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def make_schematic(level, box, options, schematic, offset):
	newBox = BoundingBox((0,0,0), (schematic.Width,schematic.Height,schematic.Length))
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(schematic, newBox, (box.minx+offset[0], box.miny+offset[1], box.minz+offset[2]),b)
	level.markDirtyBox(box)

def perform(level, box, options):
	path = "stock-schematics/library/"
	house = path+"Indrae_Library.schematic"
	farm = path+"farm-wheat.schematic"
	ufo = path+"flying-saucer-alien.schematic"
	
	houseSchematic = MCSchematic(filename=house)
	farmSchematic = MCSchematic(filename=farm)
	ufoSchematic = MCSchematic(filename=ufo)

	make_schematic(level, box, options, houseSchematic, (0,0,0))
	make_schematic(level, box, options, farmSchematic, (40,0,0))
	make_schematic(level, box, options, ufoSchematic, (0,50,0))
