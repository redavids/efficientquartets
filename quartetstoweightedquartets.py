import sys
import dendropy
import copy
#this script is for taking a list of QMC formatted quartets and turning them into wQMC formatted quartets by weight=frequency


infile = str(sys.argv[1])

outfile = str(sys.argv[2])

H = open(infile,'r')

rawlist = [line.split() for line in H.readlines()]

d = {}

H.close()

rawcopy = copy.deepcopy(rawlist)

while len(rawcopy)>0:
    quartet = rawcopy.pop(0)[0]
    if quartet in d:
        d[quartet] = d[quartet]+1
    else:
        d[quartet] = 1

G = open(outfile,'w')

for i in d.keys():
    G.write(str(i) + ':' + str(d[i])+' \n')    

G.close()



