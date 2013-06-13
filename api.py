from optparse import OptionParser

op = OptionParser()
op.add_option("-e","--endpoint")

opts,args = op.parse_args()

if not opts.endpoint:
    print "No endpoint specified! Use the -h flag to view options!"

if opts.endpoint == "projects":
    print "Projects should be output here ..."
    # Do something
elif opts.endpoint == "persons":
    print "Persons should be output here ..."
    # Do something else
elif opts.endpoint == "jobs":
    print "Jobs should be output here ..."
    # Do something else still
    
