import re

# Returns a generator object yielding project objects
def projects_gen():
    projfile = open("etc/projects","r")
    proj = Project()
    for line in projfile:
        if line == "\n":
            # Return project object and create new one
            yield proj
            proj = Project()
        if ":" in line:
            lineparts = line.split(":") 
            if len(lineparts) > 1:
                fieldname = lineparts[0].strip(" \t").lower()
                fieldval = lineparts[1].strip(" \t\n")
                if fieldname == "name":
                    # Special handling for name. Primary id should 
                    # always use id as field name.
                    setattr(proj, "id", fieldval)
                else:
                    setattr(proj, fieldname, fieldval)
    # Yield the last proj object (which will not get yielded in the 
    # loop above)
    yield proj
    projfile.close()

class Project(object):
    pass
