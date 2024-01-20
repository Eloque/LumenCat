# LumenCat
Python based laser cutter GCode generator

# Purpose
If you can't find exactly what you are searching for, did you know you can just write your own GCode generator?

This one is supposed to and currently kinda of does:

- Generate GCode that works for a Sculpfun S9, that means GRBL1.1
- Use basic SVG formats for lines and texts
- Converts, inverts and SVG to points and then to GCode

It does not but really should:

- Offer some sort of GUI
- Save the files it generates, instead of just outputting to terminal
- Be able to open files instead of just having to hard code it
- Generate material test files to test materials

It does not, probably should and might later:

- Have some sort of way to draw shapes and place texts via GUI. 
- Control the cutter via USB/Serial

# How does it do it
As adequatly as I can make it. It's Python of course, but since this is my project and I don't have to take anything into account it might be a bit non-standard. Currently, it is implementing a couple of classes:

- LaserProject, a container that holds a bunch of settings and objects
- LaserObject, a representation of some SVG data and desired speed and power
- LaserTextObject, derived from LaserObject. This is text, with the ability to convert it to just path data. So it represents itself as a list of LaserObjects.

The LaserProject has functions to convert all the SVGs to points and the points to GCode. 

Al this relies on some external functions, including a way to convert text to glyps and beziers to lines. The latter one is only very lightly understood by me. Shame, I used to be good at math. 

So, create a LaserProject, add LaserObjects and LaserTextObejects to it and call the get_gcode() function and it works. Sort of. Tests so far are looking good.

# What did I use
Open source is a wonderfull thing. But it is proper to refer to some things used:

For the GUI, that most wonderfull and devastating invention I used:
- https://github.com/TomSchimansky/CustomTkinter by @TomSchimansky
- https://github.com/Akascape/CTkXYFrame by @Akascape


