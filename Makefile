

.PHONY: 


tableau:
	cd py && python mmparser.py -n > ../csv/nodes.csv
	cd py && python mmparser.py -e > ../csv/edges-tree.txt
	cd py && python mmparser.py -t > ../csv/edges-trans.txt

graph:
	 tail -n +3 csv/nodes.csv > csv/nodes.tmp.csv	
	 cd csv && python ../../../botapad/botapad.py --host http://padagraph.io --key `cat ../../../key.io` --separator ';' -v --delete  fallacies ./main.txt

svg :
	python py/makesvg.py

gz :
	tar -czf patrons.tar.gz svg/niveau*.svg
	tar -czf illustrations.tar.gz svg/illustrations*.svg
	tar -czf cartes.tar.gz output/