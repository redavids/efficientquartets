#!/bin/bash
eff_on=0 #efficient quartets off by default
check_on=0 #check quartet off by default
if [ $# -eq 0 ] 
then
	echo "Need arguments in form ./treequar.sh [opts] tree_file output_file"
	exit 1
fi
while getopts ":ec" opt
do
	case $opt in
		e)
			eff_on=1
			;;
		c)
			check_on=1
			;;
		\?)
			echo "Invalid Option: -$OPTARG"
			;;
	esac
done
shift $((OPTIND-1))
arr=("$@")
infile=${arr[0]}
if [ ${#arr[@]} -eq 2 ]
then 
	outfile=${arr[1]}
else
	outfile="quarfile" #default quartet filename
fi
#intree & intree2 are input files to treedist
intree="intree"
intree2="intree2"
echo -n "`cat $infile > $intree`"
distopts="R\nD\n2\nC\nV\nY\n"


if [ $check_on -eq 1 ] #infile is a list of trees, run all in maxcut and check with treedist
then 
	echo -n "`echo -n "" > $intree2`" #clear intree2 file
	echo -n "`echo -e "\n" >> $intree`"  #put new line at end of file incase there isnt one already
	while read -r line && [[ -n $line ]]
	do
		tree=$line
		echo -n "`echo "$tree" > temp`" #input for treemeth.py
		if [ $eff_on -eq 1 ]
		then
			echo "`python2.7 treemeth.py temp $outfile eff`"
		else
			echo "`python2.7 treemeth.py temp $outfile`"
		fi	
		echo -n "`./find-cut-Linux-64 qrtt=$outfile otre=temp`" #run max cut on results
		echo -n "`cat temp >> $intree2`" #add result to intree2
	done < $intree
	echo "`echo -e $distopts | ./treedist`"
	echo "treedist run, look in outfile for result"
elif [ $eff_on -eq 1 ]
then
	echo "`python2.7 treemeth.py $infile $outfile eff`"
else
	echo "`python2.7 treemeth.py $infile $outfile`"
fi	
