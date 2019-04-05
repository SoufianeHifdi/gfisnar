#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca

from gfishnar import *

#------------------------------READ--------------------------------------------
yaml = YAML("input.yaml")
Gcode = Gcode()
gcode=Gcode.read(yaml.gcodepath)
#-----------------------------EXTRACT------------------------------------------
extract=extract(gcode,yaml.deck)
#-----------------------------GENERATE-----------------------------------------
generate= Reverse(extract.deck,yaml.deck)
#-----------------------------CALIBRATE----------------------------------------
calibrate=Calibrate(generate.deck,yaml.deck)
#-----------------------------WRITE--------------------------------------------
writer=write(generate.deck,calibrate.coord)
print 'Output file(s) is now available in the current directory'
print 'Import it into Excel, then copy-paste the content in the Fisnar software'
#-----------------------------PLOT TOOLPATH ----------------------------------
plot = Toolpath_3D_plotter(calibrate.coord)
layer_coordinates = plot.fisnar_reversed_layer_coordinates(extract.deck,generate.final_reversed_points,generate.indices_to_keep)
layer_plot = plot.layer_plot(6,layer_coordinates)
