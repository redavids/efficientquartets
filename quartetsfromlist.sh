#!/bin/bash


#$1 is file name you give as input: it should be a file containing a list of gene trees in newick format.  
#$2 is the number of gene trees in the file: be sure there are no extra spaces at the end!!!

line=0
for i in `cat /$1`; do
    ((line++))
    echo $i > foo
    python getridofedgeweights.py foo newfoo 
    #echo head -1 tmpfile
    ./treequar.sh newfoo /$1.ruth.$line
#done
cat /$1.ruth.* > /$1.listofQMCquartets
done
python quartetstoweightedquartets.py /$1.listofQMCquartets /$1.WQMCquartets
