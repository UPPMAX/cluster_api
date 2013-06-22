import re
import subprocess as sub

# Returns a generator object yielding job objects
def jobs_gen():
    job = Job()
    proc = sub.Popen(["squeue", "-ho", "%i,%P,%j,%u,%t,%M,%D,%R"], stdout = sub.PIPE, stderr = sub.PIPE)
    while True:
        line = proc.stdout.readline()
        if line != '':
            field_names = ["id", "partition", "name", "username", "state", "time_used", "num_nodes", "reason"]
            field_values = [f.strip() for f in line.split(",")]
            for field_name, field_value in zip(field_names, field_values):
                setattr(job, field_name, field_value)
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

