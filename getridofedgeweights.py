import dendropy
import sys


#Note: this only works on one tree at a time!!!! this is the replacing [&U] hack unfortunately. 
infile = str(sys.argv[1])

outfile = str(sys.argv[2])

L = dendropy.TreeList.get_from_path(infile, 'newick')

#H  = open(outfile,'w')

#for i in range(len(L)):
    #s = L[i].as_newick_string() + ';\n'
    #H.write(s)

#H.close()

L.write_to_path('middle', 'newick',suppress_edge_lengths=True)

G = open('middle','r')

S = G.read()

#S.replace('[&U] ', '')

print S

print S[5:]

G.close()

J = open(outfile, 'w')

J.write(S[5:])

J.close()

