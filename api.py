import sys
from optparse import OptionParser
from uppmax import projects, jobs

op = OptionParser()
op.add_option("-e","--endpoint")
op.add_option("--project-category",help="Can be one of: uppnex, uppnex-platform, uppnex-research, course, uppmax, uppmax-research, uppmax-snic")
op.add_option("--job-fields", help="Fields to output for job. Default: id. Available: id, partition, name, username, state, time_used, num_nodes, reason. Multiple fields can be specified, and should be separated by comma.")

opts,args = op.parse_args()

if not opts.endpoint:
    sys.exit("No endpoint specified! Use the -h flag to view options!")

def print_name(obj):
    if hasattr(obj, "name"):
        print obj.name

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
            print_name(proj)
    else:
        # Output all projects
        for proj in projects.projects_gen():
            print_name(proj)

elif opts.endpoint == "persons":
    print "Persons should be output here ..."
    # Do something else

elif opts.endpoint == "jobs":
    for job in jobs.jobs_gen():
        outputs = []
        job_fields = opts.job_fields.split(",")
        if job_fields == None:
            outputs.append(job.id)
        else:
            for field_name in job_fields:
                outputs.append(getattr(job, field_name))
        print "\t".join(outputs)


elif opts.endpoint == "modules":
    print "Modules should be output here ..."
    # Do something else still

elif opts.endpoint == "executables":
    print "Executables should be output here ..."
    # Do something else still

    

# Returns the current user's projects
#groups|tr " " "\n"|grep -P "^(staff|[abgsp][0-9]+)$"
