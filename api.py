from optparse import OptionParser
from uppmax import projects

op = OptionParser()
op.add_option("-e","--endpoint")

for proj in projects.projects_gen():
        if hasattr(proj, "name"):
                    print proj.name


opts,args = op.parse_args()

if not opts.endpoint:
    print "No endpoint specified! Use the -h flag to view options!"

if opts.endpoint == "projects":
    # Output all projects
    for proj in projects.projects_gen():
        if hasattr(proj, "name"):
            print proj.name
elif opts.endpoint == "persons":
    print "Persons should be output here ..."
    # Do something else
elif opts.endpoint == "jobs":
    print "Jobs should be output here ..."
    # Do something else still
    
