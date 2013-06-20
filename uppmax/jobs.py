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
    def __init__(self):
        self.id = None
        self.partition = ""
        self.name = ""
        self.username = ""
        self.state = None
        self.time_used = None
        self.num_nodes = None
        self.reason = ""

