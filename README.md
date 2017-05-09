# Fallacies
Reprository to manage the fallacies taxonomy and related scripts



## Python

convert mm to csv 

    $ # nodes
    python mmparser.py -n > nodes.csv
    $ # tree link
    python mmparser.py -e > edges-tree.txt
    $ # trans link
    $ python mmparser.py -t > nodes-trans.txt


## CSV 

fichier d import botapad



fichiers genéré via le script python mmparser.py

./csv 
  nodes.csv
  edges-tree.txt
  edges-trans.txt
  

## Fichier editable en ligne

Pour traduction et complement d informations sur les nodes/cartes 

https://framacalc.org/mu7kkecijo


## SVG

https://drive.google.com/open?id=0B37iA9aO7RWhOUpqdG9XMXRyQVk

L'idée c'est qu'on à 4 type de carte différents

* `famille`: pas de cercle centraux, quatre coins, les sous familles en blanc dans le liserai gauche

* `sous famille`: un petit oeuf central, deux coins, la famille en couleur sur fond blanc dans le liserai du bas, les sous familles en blanc, sauf la sous famille concernée en couleur sur fond blanc, les sous sous familles en blanc dans le liserai droit

* `sous sous famille`: un oeuf central plus gros, un coins, la famille en couleur sur fond blanc dans le liserai du bas, les sous familles en blanc, sauf la sous famille concernée en couleur sur fond blanc, les sous sous familles en blanc dans le liserai droit sauf la sous sous famille concernée en couleur sur fond blanc

* `argument exemple`: un oeuf central gros, pas de coins, la famille en couleur sur fond blanc dans le liserai du bas, les sous familles en blanc, sauf la sous famille concernée en couleur sur fond blanc, les sous sous familles en blanc dans le liserai droit sauf la sous sous famille concernée en couleur sur fond blanc


## Graphs

Convertion des fichiers csv vers un graph padagraph.

$ python ../../../botapad/botapad.py --host http://localhost:5000 --key `cat ../../../key.local` --separator ';' -v --delete  fallacies ./main.txt



TODO
