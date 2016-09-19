#!/bin/bash
for i in {1..50}; do
	~/code/wQMC/max-cut-tree qrtt=/Users/ruthdavidson/code/DATA/ASTRAL2.50Taxa/model.50.2000000.0.000001.true/$i/truegenetrees weights=on otre=~/DATA/ASTRAL2.50TaxaForEfficientQuartets/model.50.2000000.0.000001.true/$i/9.18.16.all.true.wQMC.tree

	~/code/compareTrees/compareTrees.missingBranchRate ~/DATA/ASTRAL2.50TaxaForEfficientQuartets/model.50.2000000.0.000001.species/$i/s_tree.trees ~/DATA/ASTRAL2.50TaxaForEfficientQuartets/model.50.2000000.0.000001.true/$i/9.18.16.all.true.wQMC.tree > ~/DATA/ASTRAL2.50TaxaForEfficientQuartets/model.50.2000000.0.000001.true/$i/6.2.16.efficient.missingBranchRate

done
