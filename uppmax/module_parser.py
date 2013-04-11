#!/usr/bin/python

import re
import subprocess as sub

infile = open(".module_avail_bioinfo-tools.cache","r")

tool_groups = {} 
tools = {}
for line in infile:
    if line.startswith("/"):
        tool_groupname = line.split("/")[-1].strip("\n:")
        tools = {}
        tool_groups[tool_groupname] = tools
    else:
        if "/" in line:
            tool, version = line.split("/")
            tool = tool.strip("\n")
            version = version.strip("\n")
            if tool in tools:
                tools[tool].append(version)
            else:
                tools[tool] = [version]

for group, tools in tool_groups.iteritems():
    print "-"*80
    print "%s:\n%s" % (group, str(tools))
