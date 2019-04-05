#-*- coding: utf-8 -*-
#@author: aziz-yamar.gueye@polyml.ca

import re

## Class to rewrite the Gcode to include changed coordinates and extrusion for curved toolpath
class GCODErewriter():

	## Constructor
    # @param Gcodepath The path of the GCODE file in the YAML reader
    # @param new_points The new points from reverse class, more specifically new_points method
    # @param new_E The new extrusion values from reverse class, more specifically new_E method
    def __init__(self,Gcodepath,new_points,new_E):
        self.Gcode_lines = GCODErewriter.read(self,Gcodepath)
        self.new_lines = GCODErewriter.coordinates_modify(self,self.Gcode_lines,new_points, new_E)
        self.final_lines = GCODErewriter.E_modify(self,self.new_lines,new_E)
        self.write = GCODErewriter.rewrite(self, self.final_lines)

    ## Reads the GCODE line by line
    # @param Gcodepath the path of the Gcode file
    def read(self,Gcodepath):
        f = open(Gcodepath, 'r')
        Gcode_lines = f.readlines()
        return Gcode_lines
        f.close()


    ## Modifies the XYZ coordinates for each Gcode line
    # @param Gcode_lines the lines of Gcode to modify
    # @param new_points the new coordinates to write in new Gcode
    def coordinates_modify(self,Gcode_lines,new_points,new_E):
        new_lines = []
        points = []
        j= 0
        e= 0

        for i in range (0,len(Gcode_lines)):
            # Finds pattern, example of pattern: G0 X112.210 Y200.321
            new_line = 0
            pattern=re.compile(r'\bG\d+\s\b(X\d+\.\d+\s\bY\d+\.\d+\s)\b')
            match=pattern.findall(Gcode_lines[i])
            if len(match) != 0:
                indices=pattern.finditer(Gcode_lines[i])
                for index in indices:
                    start_index = index.start(1)
                    end_index = index.end(1)

                    #while j <= len(new_points)-1:

                    while new_points[j][3] == new_points[j+1][3]:
                        new_line = Gcode_lines[i][0:start_index] + 'X'+str(new_points[j][0])+' Y'+str(new_points[j][1])+ ' Z'+str(new_points[j][2]) +' '+ Gcode_lines[i][end_index:]
                        new_lines.append(new_line)
                        if j+1 < len(new_points)-1:
                            j +=1
                        #elif j+1 == len(new_points)-1:
                        #    new_line = Gcode_lines[i+1][0:start_index] + 'X'+str(new_points[j+1][0])+' Y'+str(new_points[j+1][1])+ ' Z'+str(new_points[j+1][2]) +' '+ Gcode_lines[i+1][end_index:]
                        #    new_lines.append(new_line)
                        #    j = j+1
                        #    break
                        else:
                            j = j+1
                            break

                    new_line = Gcode_lines[i][0:start_index] + 'X'+str(new_points[j][0])+' Y'+str(new_points[j][1])+ ' Z'+str(new_points[j][2]) +' '+ Gcode_lines[i][end_index:]
                    new_lines.append(new_line)
                    if j+1 < (len(new_points)-1):
                        j +=1



            # Finds pattern, example of pattern: G0 E3.0450
            #pattern=re.compile(r'\bG\d+\s\b(E\d+\.\d+\s)\b')
            #match=pattern.findall(Gcode_lines[i])
            #if len(match) != 0:
                #indices=pattern.finditer(Gcode_lines[i])
                #for index in indices:
                    #start_index = index.start(1)
                    #end_index = index.end(1)
                    #new_line = Gcode_lines[i][0:start_index] + 'E'+str(new_E[e][0]) +' '+ Gcode_lines[i][end_index:]
                    #new_lines.append(new_line)
                    #e += 1

            # Finds pattern, example of pattern: layer 1,
            pattern=re.compile(r'\b(layer+\s\d)\b')
            match=pattern.findall(Gcode_lines[i])
            if len(match) != 0:
                indices=pattern.finditer(Gcode_lines[i])
                for index in indices:
                    start_index = index.start(1)
                    end_index = index.end(1)
                    new_line = Gcode_lines[i][0:end_index]+ Gcode_lines[i][-1]
                    new_lines.append(new_line)

            # Finds pattern, example of pattern: G0 Z3.0450
            pattern=re.compile(r'\bG\d+\s\b(Z\d+\.\d+\s)')
            match=pattern.findall(Gcode_lines[i])
            if len(match) != 0:
                new_line = -1

            if new_line == 0:
                new_line = Gcode_lines[i]
                new_lines.append(new_line)
            #if new_line != -1:
                #new_lines.append(new_line)
        #line_index = line_index +len(Gcode_lines[i])
        return new_lines

    ## Modifies the E values for each Gcode line
    # @param Gcode_lines the lines of Gcode to modify
    # @param new_E the new E values to write in new Gcode
    def E_modify(self,Gcode_lines,new_E):
        j= 0
        new_lines=[]
        for i in range (0,len(Gcode_lines)):
        	# Finds pattern, example of pattern: G0 X112.210 Y200.321 E44.44
            pattern=re.compile(r'\bG\d+\s\bX\d+\.\d+\s\bY\d+\.\d+\s\bZ\d+\.\d+\s\b(E\d+\.\d+)\b')
            # Only returns the first group (E\d+\.\d+)
            match=pattern.findall(Gcode_lines[i])
            if len(match) != 0:
                E=pattern.finditer(Gcode_lines[i])
                for e in E:
                    start_index = e.start(1)
                    end_index = e.end(1)
                    new_line = Gcode_lines[i][0:start_index] + 'E'+str(new_E[j][0]) + Gcode_lines[i][end_index:]
                    if j+1 <= len(new_E)-1:
                        j += 1
            else:
                new_line = Gcode_lines[i]
            new_lines.append(new_line)
        return new_lines

    ## Writes the GCODE line by line
    # @param new_lines the modified lies of Gcode ready to be written
    def rewrite(self,new_lines):
        f = open('Gcode_curved.gcode','w+')
        for line in new_lines:
            f.write(line)
        f.close()


    #def make_lines(self,extractDeck,generateDeck):