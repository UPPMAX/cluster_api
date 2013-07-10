import sys
import re
from optparse import OptionParser
from uppmax import projects, jobs


def main():
    opts = parse_args()
    # Execute function based on endpoint command line option
    endpoint_to_execute = "exec_" + opts.endpoint + "_endpoint"
    gen_obj = globals()[endpoint_to_execute](opts) # Call function based on function name in string FIXME: Security hole!

    # Set default output format if no format is specified
    if opts.format:
        format = opts.format
    else:
        format = "tab"

    # Choose how to print based on output format parameter
    if format == "tab":
        print_tabular(gen_obj)
    elif format =="xml":
        print_xml(gen_obj, opts.endpoint)
    else:
        print ("Format '%s' not (yet?) implemented! Use the -h flag to "
               "view available options!") % opts.format

def exec_clusters_endpoint(opts):
    for cluster in [ { "id" : "kalkyl",
                       "maxcpus" : "8",
                       "maxnodes" : "348"}, 
                     { "id" : "tintin",
                       "maxcpus" : "16",
                       "maxnodes" : "160"}]:
        yield cluster

def exec_projects_endpoint(opts):
    if opts.project_category:
        if opts.project_category == "uppnex":
            projname_pattern = "[ab][0-9]{6,7}"
        elif opts.project_category == "uppnex-platform":
            projname_pattern = "[a][0-9]{6,7}"
        elif opts.project_category == "uppnex-research":
            projname_pattern = "[b][0-9]{6,7}"
        elif opts.project_category == "course": 
            projname_pattern = "[g][0-9]{6,7}"
        elif opts.project_category == "uppmax":
            projname_pattern = "[ps][nic0-9]{5,15}"
        elif opts.project_category == "uppmax-research":
            projname_pattern = "[p][0-9]{6,7}"
        elif opts.project_category == "uppmax-snic":
            projname_pattern = "[s][nic0-9\-]{5,15}"
        else:
            sys.exit(("Error: Project category is none of the allowed ones: uppnex, "
                      "uppnex-platform, uppnex-research, course, uppmax, "
                      "uppmax-research, uppmax-snic"))

        for proj in projects.projects_gen():
            if hasattr(proj, "id") and re.match(projname_pattern, proj.id):
                # Only id field implemented so far
                yield { "id" : proj.id }
    else:
        # Output all projects
        for proj in projects.projects_gen():
            if hasattr(proj, "id"):
                # Only id field implemented so far
                yield { "id" : proj.id }


def exec_jobs_endpoint(opts):
    for job in jobs.jobs_gen():
        outputs = {}
        if opts.job_fields == None:
            outputs["id"] = job.id
        else:
            job_fields = [f.strip() for f in opts.job_fields.split(",")]
            for field_name in job_fields:
                outputs[field_name] = getattr(job, field_name)
        yield outputs


def exec_persons_endpoint(opts):
    print "Persons endpoint not yet implemented"


def exec_modules_endpoint(opts):
    print "Modules endpoint not yet implemented"


def exec_executables_endpoint(opts):
    print "Executables endpoint not yet implemented"


def print_tabular(generator_obj):
    sep = "\t"
    for field in generator_obj:
        values = [v for k,v in field.iteritems()]
        print sep.join(values)


def print_xml(generator_obj, endpoint_name):
    object_type = endpoint_name[:-1] # Remove the trailing 's' in endpoint name
    print "<clusterapi>"
    print "<%ss>" % object_type
    for items in generator_obj:
        xmlline = "<%s " % object_type
        line_parts = ["%s=\"%s\"" % (k,v) for k,v in items.iteritems()]
        xmlline += " ".join(line_parts) + " />"
        print xmlline
    print "</%ss>" % object_type
    print "</clusterapi>"


def parse_args():
    '''
    Parse command line options
    '''
    op = OptionParser()
    op.add_option("-e","--endpoint")
    op.add_option("--project-category",help=("Can be one of: uppnex, uppnex-platform, "
                                             "uppnex-research, course, uppmax, "
                                             "uppmax-research, uppmax-snic"))
    op.add_option("--job-fields", help=("Fields to output for job. Default: id. "
                                        "Available: id, partition, name, username, "
                                        "state, time_used, num_nodes, reason. Multiple "
                                        "fields can be specified, and should be "
                                        "separated by comma."))
    op.add_option("--job-filters", help=("Filter jobs based on field values")) # TODO: Add more text here
    op.add_option("--format", "-f", help=("Specify the output format. Available formats "
                                          "are tab (default), xml and json"))
    opts,args = op.parse_args()
    return opts

    if not opts.endpoint:
        sys.exit("No endpoint specified! Use the -h flag to view options!")


if __name__ == '__main__':
    main()
