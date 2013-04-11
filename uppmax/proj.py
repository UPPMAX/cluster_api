import re

def main():
    for p in gen_projects():
        if re.match("[ab][0-9]{7}", p.name):
            print p.name

def gen_projects():
    pf = open("etc/projects","r")
    p = Project()
    for l in pf:
        if l == "\n":
            yield p
            p = Project()
        if ":" in l:
            bits = l.split(":") 
            if len(bits) > 1:
                k = bits[0].strip(" \t").lower()
                v = bits[1].strip(" \t\n")
                setattr(p, k, v)

class Project(object):
    pass

if __name__ == '__main__':
    main()
