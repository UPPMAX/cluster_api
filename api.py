import sys
from optparse import OptionParser
from uppmax import projects

op = OptionParser()
op.add_option("-e","--endpoint")
op.add_option("-c","--category",help="Can be one of: uppnex, uppnex-platform, uppnex-research, course, uppmax, uppmax-research, uppmax-snic")

opts,args = op.parse_args()

if not opts.endpoint:
    sys.exit("No endpoint specified! Use the -h flag to view options!")

def print_projname(proj):
    if hasattr(proj, "name"):
        print proj.name

if opts.endpoint == "projects":
    if opts.category:
        if opts.category == "uppnex":
            projname_pattern = "[ab][0-9]{6,7}"
        elif opts.category == "uppnex-platform":
            projname_pattern = "[a][0-9]{6,7}"
        elif opts.category == "uppnex-research":
            projname_pattern = "[b][0-9]{6,7}"
        elif opts.category == "course": 
            projname_pattern = "[g][0-9]{6,7}"
        elif opts.category == "uppmax":
            projname_pattern = "[ps][nic0-9]{5,15}"
        elif opts.category == "uppmax-research":
            projname_pattern = "[p][0-9]{6,7}"
        elif opts.category == "uppmax-snic":
            projname_pattern = "[s][nic0-9\-]{5,15}"
        else:
            sys.exit("Error: Project category is none of the allowed ones: uppnex, uppnex-platform, uppnex-research, course, uppmax, uppmax-research, uppmax-snic")

        for proj in projects.projects_by_regex_gen(projname_pattern):
            print_projname(proj)
    else:
        # Output all projects
        for proj in projects.projects_gen():
            print_projname(proj)
elif opts.endpoint == "persons":
    print "Persons should be output here ..."
    # Do something else
elif opts.endpoint == "jobs":
    print "Jobs should be output here ..."
    # Do something else still
    

# Returns the current user's projects
#groups|tr " " "\n"|grep -P "^(staff|[abgsp][0-9]+)$"
