import re
import subprocess as sub

# Returns a generator object yielding job objects
def jobs_gen():
    job = Job()
    proc = sub.Popen(["squeue", "-ho", "%i"], stdout = sub.PIPE, stderr = sub.PIPE)
    while True:
        line = proc.stdout.readline()
        if line != '':
            job.id = line.strip()
            yield job
            job = Job()
        else:
            break

class Job():
    pass
