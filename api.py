import sys
from optparse import OptionParser
from uppmax import projects, jobs


def main():
    opts = parse_args()
    # Execute function based on endpoint command line option
    endpoint_to_execute = "exec_" + opts.endpoint + "_endpoint"
    gen_obj = globals()[endpoint_to_execute](opts) # Call function based on function name in string FIXME: Security hole!

    if opts.format:
        format = opts.format
    else:
        format = "tab"

    if format == "tab":
        print_tabular(gen_obj)
    else:
        print "Format '%s' not (yet?) implemented! Use the -h flag to view available options!" % opts.format

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

        for proj in projects.projects_by_regex_gen(projname_pattern):
             if hasattr(proj, "name"):
                yield getattr(obj, "name")
    else:
        # Output all projects
        for proj in projects.projects_gen():
            if hasattr(proj, "name"):
                yield getattr(proj, "name")


def exec_jobs_endpoint(opts):
    for job in jobs.jobs_gen():
        outputs = []
        if opts.job_fields == None:
            outputs.append(job.id)
        else:
            job_fields = [f.strip() for f in opts.job_fields.split(",")]
            for field_name in job_fields:
                outputs.append(getattr(job, field_name))
        yield "\t".join(outputs)


def exec_persons_endpoint(opts):
    print "Persons endpoint not yet implemented"


def exec_modules_endpoint(opts):
    print "Modules endpoint not yet implemented"


def exec_executables_endpoint(opts):
    print "Executables endpoint not yet implemented"


def print_tabular(generator_obj):
    for item in generator_obj:
        print item


# Helper functions


def print_field(obj, field_name):
    if hasattr(obj, field_name):
        print getattr(obj, field_name)


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
    op.add_option("--format", "-f", help=("Specify the output format. Available formats "
                                          "are tab (default), xml and json"))
    opts,args = op.parse_args()
    return opts

    if not opts.endpoint:
        sys.exit("No endpoint specified! Use the -h flag to view options!")


if __name__ == '__main__':
    main()
