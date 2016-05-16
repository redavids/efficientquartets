#!/bin/bash


#$1 is file name you give as input: it should be a file containing a list of gene trees in newick format.  
#$2 is path the folder where you want to work on your datai

#if [ $# -lt 2 ]; then
  #echo 1>&2 "this bash script takes two arguments: the name of the file of gene trees in newick format and the path to the folder containing it"
  #exit 2

line=0
for i in `cat $2/$1`; do
    ((line++))
    echo $i > $2/doody
    python getridofedgeweights.py $2/doody $2/newdoody 
    #echo head -1 tmpfile
    /Users/ruthdavidson/code/treemeth/treequar.sh $2/newdoody  $2/$1.ruth.$line
done
cat $2/$1.ruth.* > $2/$1.listofQMCquartets
python quartetstoweightedquartets.py $2/$1.listofQMCquartets $2/$1.efficientWQMCquartets
#rm /Users/ruthdavidson/code/treemeth/$1.listofQMCquartets
rm $2/$1.ruth.*
