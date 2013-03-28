import subprocess as sub
import re
import sys


proc = sub.Popen("getent group", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)

def gen_lines(proc):
    line = True
    while line:
        line = proc.stdout.readline()
        yield line

groups_gen = (line.split(":")[0] for line in gen_lines(proc))
proj_pat = "([abgps][0-9\-]{6,20}|snic[0-9\-]+|staff)"
projects_gen = (g for g in groups_gen if re.match(proj_pat, g))
for p in projects_gen:
    print p
