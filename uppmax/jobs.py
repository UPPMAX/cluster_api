import re
import subprocess as sub

# Returns a generator object yielding job objects
def jobs_gen():
    proc = sub.Popen(["squeue", "-ho", "%i"], stdout = sub.PIPE, stderr = sub.PIPE)
    while True:
        line = proc.stdout.readline()
        if line != '':
            yield line.strip()
        else:
            break
