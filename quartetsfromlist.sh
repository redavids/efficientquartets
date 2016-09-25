#!/bin/bash


#$1 is file name you give as input: it should be a file containing a list of gene trees in newick format.  
#$2 is the number of gene trees in the file: be sure there are no extra spaces at the end!!!

line=0
for i in `cat $1`; do
    ((line++))
    echo $i > foo
    python getridofedgeweights.py foo newfoo 
    #echo head -1 tmpfile
    /home/redavid2/phylogenetics/efficientquartets/treequar.sh /home/redavid2/phylogenetics/efficientquartets/newfoo /home/redavid2/phylogenetics/efficientquartets/$1.ruth.$line
done
cat /home/redavid2/phylogenetics/efficientquartets/efficientquartets/$1.ruth.* > /home/redavid2/phylogenetics/efficientquartets/$1.listofQMCquartets
python quartetstoweightedquartets.py /home/redavid2/phylogenetics/efficientquartets/$1.listofQMCquartets /home/redavid2/phylogenetics/efficientquartets/$1.WQMCquartets
