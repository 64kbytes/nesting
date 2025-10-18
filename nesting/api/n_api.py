from nesting.parser import gcodeparser


def gcode_to_shape(file):
    """Returns a list of shapes [Shape1[...], Shape2[...]] or an empty list
    if no shapes were found in the given file
    """
    gcode = None

    with open(file, "r") as f:
        gcode = f.read()

    if gcode:
        xtr = gcodeparser.ShapeExtractor(gcode, suppressLeadIn=True)
        xtr.run()

        return xtr.get_shapes()
