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
            #print " -" , key, carte[key]
            xml = re.sub("!%s"% key, carte[key] , xml)
    return xml
    
def set_illustration(carte, soup, svg):
    # ILLUSTRATION
    svgpath = soup.find(attrs={'id':'illustration'})
    if 'style' in svgpath.attrs :
        style = svgpath.attrs['style'].lower()
        style = re.sub("(?<=fill:)#[a-f0-9]+",  "#000000", style )
        svgpath.attrs['style'] = style

    svgpath.append(svg)
    

def set_color(soup, color):
    # corners color
    svgpath = soup.find_all('path')

    for p in svgpath:
        style = p.attrs['style'].lower()
        style = re.sub("(?<=fill:)#[a-f0-9]+",  color, style )
        p.attrs['style'] = style

    # rect color
    svgrect = soup.find_all('rect')[1:]
    for p in svgrect:
        if 'style' in p.attrs:
            style = p.attrs['style'].lower()
        fillwhite = re.match('fill:#ffffff;', style)
        if not fillwhite:
            style = re.sub("(?<=fill:)#[a-f0-9]+",  color, style )
        style = re.sub("(?<=stroke:)#[A-Fa-f0-9]+", color, style )
        p.attrs['style'] = style
    # oval 
    oval = soup.find(attrs={'id':'oval'})
    if oval and 'style' in oval.attrs:
        style = oval.attrs['style'].lower()
        style = re.sub("(?<=fill:)#[a-f0-9]+",  color, style )
        style = re.sub("(?<=stroke:)#[A-Fa-f0-9]+", color, style )
        oval.attrs['style'] = style

def gener_svg(patron, cartes, illustrations, output):

    for carte in cartes:
        xml = "%s" % patron
        
        xml = set_texts(carte, xml)

        soup =  BeautifulSoup(xml, 'xml')
        
        set_color(soup, carte['color'])

        print carte['path'],  carte['PK'],  carte['text'], "[X]" if carte['PK'] in illustrations else "-"
        if carte['PK'] in illustrations:
            set_illustration(carte, soup, illustrations[carte['PK']])
        #else :
            #print "missing %s illustration" % carte['path']
        
        outpath = "%s/%s.svg" % (output, carte['path'])
        with open( outpath , 'wb') as out:
            out.write("%s" % soup)



def html_table_a_img(allcartes):
    def ichunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    _url = lambda u : "http://localhost:8000/output/%s.svg"% u

    for i in range(1,8):
        cartes = [ c for c in allcartes if c['path'][0] == "%s" % i ]
        paths = sorted([ c['path'] for c in cartes])
        imgs = [" <a href='%s' target='iframe'> <img src='%s' title='%s'/> </a>" % (_url(c),_url(c),c) for c in paths]

        print "## %s" % i
        print "| | | | | \n| --- | --- | --- | --- |"
        chunks = [ " %s %s " % (e[0], e[1]) for e in zip(paths, imgs) ]
        for e in ichunks(chunks, 4):
            print "| %s | " %  "|".join( e )
            
def main():

    output = "output"
    path_argumentum = "csv/argumentum.csv"
    path_illustrations = [ "svg/illustrations %s.svg" % e for e in 
        ['insuffisance', 'influence', 'math', 'paralogisme', 'langue', 'tricherie', 'obstruction'] ]
    path_niveaux = ["svg/niveau%s.svg" % i for i in range(1,5)]


    rows = csvparser.read(path_argumentum, 'fr')
    allcartes = csvparser.get_cartes(rows)

    
    idx = csvparser.makeidx(allcartes)
    idxpk = { c['PK']: c  for c in allcartes}

    illustrations = {}
    for i,e in enumerate(path_illustrations):
        print i, e 
        soup = bs(e)
        gs = [ g for g in soup.find_all('g') ]
        if len(gs) == 1 : 
            gs = [ g for g in gs.find_all('g') ]
        for g in gs:
            #del g.attrs['transform']
            illustrations[g.attrs['id']] = g
            print g.attrs['id']
    print len(gs), "\n", sorted(illustrations.keys())
    
    

    # ============
    for i in range(1,7):
        cartes = [ carte for carte in allcartes if carte['depth'] == i]
        #for c in cartes: print c['f'], c['sf'], " ; " ,c['path'], ' - ',c['depth']
        print "niveau %s" % i, len(cartes)
        if i > 4 : i = 4
        patron = readsvg(path_niveaux[ i-1 ])
        gener_svg(patron, cartes, illustrations, output)

    print len(allcartes), ' cartes', len([ c for c in allcartes if c['PK'] in illustrations ]), " illustrations"

    #html_table_a_img(allcartes)

main()