#!/bin/bash

#$1 is the name of the file that you're using, $2 is the path the folder containing that file, don't type the / between the $1 and $2! (weird, I know)

/Users/ruthdavidson/code/quartet_scores/quartet-controller.sh $2/$1 $2/$1.all.quartets

cat $2/$1.all.quartets | sed s/"(("//g | sed s/"),("/"|"/g | sed s/")); "/":"/g | sed '/|/!d' > $2/$1.allWQMCquartets
