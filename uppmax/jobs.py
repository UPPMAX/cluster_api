import re
import subprocess as sub

# Returns a generator object yielding job objects
def jobs_gen():
    job = Job()
    proc = sub.Popen(["squeue", "-o", "'%i'"], stdout = sub.PIPE, stderr = sub.PIPE)
    for line in proc.stdout.readline():
        yield line

class Job():
    

if __name__ == '__main__':
    main()
