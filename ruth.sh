#!/bin/bash

# rep is number species trees, genes number of locus trees per species trees, species number of species, b is distribution of birth rates, t is distribution of maximum tree lengths, tr is distribution of transfer rates 
rep=10
genes=1000
species=50
for b in 0.000001 0.0000001; do
	for t in 500000 2000000 10000000; do
		for tr in 0.00000001 0.000000001; do 
		       ~/code/simphy-project/src/simphy -rs $rep -rl U:$genes,$genes -rg 1 -st U:$t,$t -si U:1,1 -sl U:$species,$species -sb U:$b,$b -cp U:200000,200000  -hs L:1.5,1 -hl L:1.2,1 -hg l:1.4,1 -cu E:10000000 -so U:1,1 -od 1 -or 0 -v 3  -cs 293745 -o model.$species.$t.$b.$tr -lt U:$tr,$tr -lk 1| tee log.$species.$t.$b.$tr;
			#perl post_stidsim.pl `pwd`/model.$species.$t.$b.$tr 1 # You can comment this line in your initial tests
			for r in `ls -d model.$species.$t.$b.$tr/*`; do
				cat $r/g_trees*.trees > $r/truegenetrees;
				rm  $r/g_trees*.trees;
			done
			echo look at model.$species.$t.$b.$tr/*/l_trees.trees for figuring out the number of transfer events
		done
	done
done

