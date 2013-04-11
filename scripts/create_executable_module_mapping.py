#!/usr/bin/python
# (c) Samuel Lampa, 2013, UPPMAX
# Script that creates a file containing a module name on the first column on 
# each line, followed by all possible binaries of that file, separated by colon.
import subprocess as s
import re

def main():
    mods = {}
    modfile = open("../etc/modulescache","r")
    for l in modfile:
        mod = l.split("/")[0]
        mods[mod] = []

    print mods

    for modname, mod in mods.iteritems():
        output = run("/usr/share/Modules/bin/modulecmd bash show " + modname + " 2>&1")
        outlines = output.split("\n")
        for l in outlines:
            if "prepend-path" in l or "append-path" in l:
                print "Line: " + l
                matches = re.findall("\/.*$", l)
                print "Matches: " + str(matches)

def run(cmd):
    #print("Now executing command: %s" % cmd)
    p = s.Popen(cmd, shell=True, stdout=s.PIPE, stderr=s.PIPE)
    stdout, stderr = p.communicate()
    return stderr

#function module_bins() {
#    { for mod in $(cat ../etc/modulescache|grep -v ":"|grep -oP "^[a-zA-Z][a-zA-Z0-9\-\_]*"|grep -v "/"|sort|uniq); do 
#        echo $mod":"$(module show $mod 2>&1|grep prepend-path|grep -oP "\/[^\:]+"|sort|uniq|xargs ls|tr "\n" ":"); done; 
#    } 2>/dev/null 
#}
#
#function bin_module_map() {
#    read line;
#    mod=$(echo $line|grep -oP "^[^\:]+");
#    for bin in $(echo $line|tr ":" " "); do
#        echo "$bin:$mod";
#    done;
#}
#
#{ for line in $(module_bins); do 
#    echo $line|bin_module_map;
#done; } | grep -v bioinfo-tools|grep -v modules|grep -v "\."

def uniq(a_list):
    return list(set(a_list))

if __name__ == '__main__':
    main()
