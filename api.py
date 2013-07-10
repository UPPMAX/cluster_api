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
                       "maxnodes" : "348",
                       "partitions" : [ "core", "node", "devel" ]}, 
                     { "id" : "tintin",
                       "maxcpus" : "16",
                       "maxnodes" : "160",
                       "partitions" : [ "core", "node", "devel", "gpu" ]}]:
        if opts.current:
            if cluster["id"] == "kalkyl": # FIXME: Don't hard-code
                yield cluster
        else:
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
        values = [stringify_value(v) for k,v in field.iteritems()]
        print sep.join(values)


def print_xml(generator_obj, endpoint_name):
    object_type = endpoint_name[:-1] # Remove the trailing 's' in endpoint name
    print "<clusterapi>"
    print "<%ss>" % object_type
    sub_collections = {}
    for items in generator_obj:
        line_parts = []
        xmlline = "<%s " % object_type
        for k, v in items.iteritems():
            if type(v) is str:
                line_parts.append("%s=\"%s\"" % (k,v))
            elif type(v) is list:
                sub_collections[k] = v
        xmlline += " ".join(line_parts)
        if len(sub_collections) > 0:
            xmlline += ">\n"
            for sub_collection_name, sub_collection in sub_collections.iteritems():
                sub_collection_item_name = sub_collection_name[:-1]
                xmlline += "<%s>\n" % sub_collection_name
                for item in sub_collection:
                    xmlline += "<%s>%s</%s>\n" % (sub_collection_item_name,item,sub_collection_item_name)
                xmlline += "</%s>\n" % sub_collection_name
            xmlline += "</%s>" % object_type
        else:
            xmlline += " />"
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
    op.add_option("--current", "-c", action="store_true", dest="current",
            help=("Use the current default."
                  "For clusters this means the current cluster."
                  "For users, this means the currently logged in user."))
    opts,args = op.parse_args()
    return opts

    if not opts.endpoint:
        sys.exit("No endpoint specified! Use the -h flag to view options!")


def stringify_value(value):
    if type(value) is str:
        return value
    if type(value) is list:
        return ",".join(value) 
    else:
        return str(value)


if __name__ == '__main__':
    main()
