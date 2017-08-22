import re
import csvparser
from bs4 import BeautifulSoup


KEYS = ['fam_num', 'fam_text',
            'text', 'txt1', 'txt2', 'desc', 'example',
            'sfam_1', 'sfam_2', 'sfam_3',
            'ssfam_1', 'ssfam_2', 'ssfam_3' ]

def bs(path):
    # load illustration
    soup = BeautifulSoup(open(path ), 'xml')
    return soup

def readsvg(path):
    with open(path, 'r') as f:
        c = f.read()
    return c
    
"""
samples ;
    map(lambda v: v.attrs['id'], e)
    e = f.find_all('path')
    v = f.find( attrs={'id':'Barrage'} )
"""

def set_texts(carte, xml):
    # texts
    for key in KEYS :
        if key in carte:
            print " -" , key, carte[key]
            xml = re.sub("!%s"% key, carte[key] , xml)
    return xml
    
def set_illustration(carte, soup, svg):
    # ILLUSTRATION
    svgpath = soup.find(attrs={'id':'illustration'})
    style = svgpath.attrs['style'].lower()
    style = re.sub("(?<=fill:)#[a-f0-9]+",  "#000000", style )
    svgpath.attrs['style'] = style
    svgpath.attrs['d'] = svg

def set_color(soup, color):
    # corners color
    svgpath = soup.find_all('path')

    for p in svgpath:
        style = p.attrs['style'].lower()
        style = re.sub("(?<=fill:)#[a-f0-9]+",  color, style )
        p.attrs['style'] = style

    # rect color
    svgrect = soup.find_all('rect')
    for p in svgrect:
        if 'style' in p.attrs:
            style = p.attrs['style'].lower()
        fillwhite = re.match('fill:#ffffff;', style)
        if not fillwhite:
            style = re.sub("(?<=fill:)#[a-f0-9]+",  color, style )
        style = re.sub("(?<=stroke:)#[A-Fa-f0-9]+", color, style )
        p.attrs['style'] = style

def gener_svg(patron, cartes, illustrations, output):

    for carte in cartes:
        print carte['path'],  carte['text']
        xml = "%s" % patron
        
        xml = set_texts(carte, xml)

        soup =  BeautifulSoup(xml, 'xml')
        
        set_color(soup, carte['color'])
        
        #set_illustration(soup, illustrations[carte['path']])

        
        outpath = "%s/%s.svg" % (output, carte['path'])
        with open( outpath , 'wb') as out:
            out.write("%s" % soup)
        
def main():
    output = "output"
    
    path_argumentum = "csv/argumentum.csv"
    path_illustrations = [ "svg/illustrations %s" % e for e in 
        ['influences', 'insuffisance', 'langue', 'math', 'obstruction', 'paralogisme', 'tricherie'] ]
    
    path_niveaux = ["svg/niveau%s.svg" % i for i in range(1,5)]

    illustrations = []

    rows = csvparser.read(path_argumentum, 'fr')
    allcartes = csvparser.get_cartes(rows)
    idx = csvparser.makeidx(allcartes)

    for c in allcartes:
        print c['f'], c['sf'], " ; " ,c['path'], ' - ',c['depth']
    print len(allcartes), ' cartes'

    # ============
    for i in range(1,7):
        cartes = [ carte for carte in allcartes if carte['depth'] == i]
        print "niveau %s" % i, len(cartes)
        if i > 4 : i = 4
        patron = readsvg(path_niveaux[ i-1 ])
        gener_svg(patron, cartes, illustrations, output)
    


main()