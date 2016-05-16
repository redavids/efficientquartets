#!/bin/bash


#$1 is file name you give as input: it should be a file containing a list of gene trees in newick format.  
#$2 is the number of gene trees in the file: be sure there are no extra spaces at the end!!!

line=0
for i in `cat $1`; do
    ((line++))
    echo $i > doody
    python getridofedgeweights.py doody newdoody 
    #echo head -1 tmpfile
    /Users/ruthdavidson/code/treemeth/treequar.sh /Users/ruthdavidson/code/treemeth/newdoody /Users/ruthdavidson/code/treemeth/$1.ruth.$line
done
cat /Users/ruthdavidson/code/treemeth/$1.ruth.* > /Users/ruthdavidson/code/treemeth/$1.listofQMCquartets
python quartetstoweightedquartets.py /Users/ruthdavidson/code/treemeth/$1.listofQMCquartets /Users/ruthdavidson/code/treemeth/$1.WQMCquartets
