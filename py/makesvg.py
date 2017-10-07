# -*- coding: utf-8 -*-
import re
import csvparser
from bs4 import BeautifulSoup


KEYS = ['fam_num', 'fam_text',
            'text', 'txt1', 'txt2', 'desc', 'example',
            'sfam_1', 'sfam_2', 'sfam_3',
            'ssfam_1', 'ssfam_2', 'ssfam_3' ]


COLORS = [
    
    # famille insuffisance
    { 'title'   : "#380050", # dessin et titre
      'text'    : "#120915", # texte sombre
      'borders' : "#a901ef", #coins et bordure
      'oval'    : "#df91ff"  # oeuf
    },
    
    # famille influence
    { 'title'   : "#504200", # dessin et titre
      'text'    : "#1e1800", # texte sombre
      'borders' : "#face00", # coins et bordure
      'oval'    : "#ffe155"  # oeuf
    },

    # famille erreur mathematique
    { 'title'   : "#054b3e", # dessin et titre
      'text'    : "#021c18", # texte sombre
      'borders' : "#00c8a6", #coins et bordure
      'oval'    : "#a4ece0"  # oeuf
    },
    
    # famille erreur de logique
    { 'title'   : "#2f5000", # dessin et titre
      'text'    : "#121e00", # texte sombre
      'borders' : "#6ab400", #coins et bordure
      'oval'    : "#b5ff4b"  # oeuf
    },

    # famille détournement de la langue
    { 'title'   : "#001350", # dessin et titre
      'text'    : "#00071e", # texte sombre
      'borders' : "#0039f0", #coins et bordure
      'oval'    : "#91abff"  # oeuf
    },

    # famille tricherie
    { 'title'   : "#47091f", # dessin et titre
      'text'    : "#240510", # texte sombre
      'borders' : "#e42065", # coins et bordure
      'oval'    : "#f5afc8"  # oeuf
    },

    # famille obstruction
    { 'title'   : "#490f07", # dessin et titre
      'text'    : "#1b0603", # texte sombre
      'borders' : "#ff2408", # coins et bordure
      'oval'    : "#f49588"  # oeuf
    },
]

def get_colors(carte):
    return COLORS[int(carte['f']) - 1 ]

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
            xml = re.sub("!%s"% key, carte[key] , xml)
    return xml
    
def set_illustration(carte, soup, svg):
    # ILLUSTRATION
    svgpath = soup.find(attrs={'id':'illustration'})
    if 'style' in svgpath.attrs :
        color = get_colors(carte)['title']
        style = svgpath.attrs['style'].lower()
        style = re.sub("(?<=fill:)#[a-f0-9]+",  color, style )
        svgpath.attrs['style'] = style

    svgpath.append(svg)

def _set_cardlift(soup, carte, prefix, display):

        active = soup.find(attrs={'id':'%s_active' % (prefix)})

        if active:
            if display == False:
                active.attrs['style'] += ";display:none;" 
                
        text = soup.find(attrs={'id':'%s' % (prefix) })
        color = get_colors(carte)['text']
        if text :
            color = color if display else "#FFFFFF" 
            style = text.attrs['style'].lower()
            style = re.sub("(?<=fill:)#[a-f0-9]+",  color, style )
            text.attrs['style'] = style

            if text : text = text.find('tspan')
            text.attrs['style'] = style
            
def set_lifts(soup, carte):
    
    tree =  [ int(e) for e in carte['path'].split('.') if len(e) ] + [0,0,0]
    f , sf , ssf = tree[:3]
    print tree, f , sf , ssf
    for i in range(1, 4):
        display =  i == sf
        print 'sfam_%s' % i, display
        _set_cardlift(soup, carte, 'sfam_%s' % i, display)
    for j in range(1, 4):
        display =  j == ssf
        print 'ssfam_%s' % j, display
        _set_cardlift(soup, carte, 'ssfam_%s' % j, display)
            
def set_color(soup, carte):
    # corners color
    colors = get_colors(carte)
    
    svgpath = soup.find_all('path')
    for p in svgpath:
        style = p.attrs['style'].lower()
        style = re.sub("(?<=fill:)#[a-f0-9]+",  colors['borders'], style )
        p.attrs['style'] = style


    # rect color
    svgrect = soup.find_all('rect')[1:]
    for p in svgrect:
        if 'style' in p.attrs:
            style = p.attrs['style'].lower()
        fillwhite = re.match('fill:#ffffff;', style)
        if not fillwhite:
            style = re.sub("(?<=fill:)#[a-f0-9]+",  colors['borders'], style )
        style = re.sub("(?<=stroke:)#[A-Fa-f0-9]+", colors['borders'], style )
        p.attrs['style'] = style

    # oval
    oval = soup.find(attrs={'id':'oval'})
    if oval and 'style' in oval.attrs:
        style = oval.attrs['style'].lower()
        style = re.sub("(?<=fill:)#[a-f0-9]+",  colors['oval'], style )
        style = re.sub("(?<=stroke:)#[A-Fa-f0-9]+", colors['oval'], style )
        oval.attrs['style'] = style

    # card title
    title = soup.find(attrs={'id':'text'})
    style = title.attrs['style'].lower()
    style = re.sub("(?<=fill:)#[a-f0-9]+",  colors['title'], style )
    #style = re.sub("(?<=stroke:)#[A-Fa-f0-9]+", colors['title'], style )
    title.attrs['style'] = style

    

def gener_svg(patron, cartes, illustrations, output):

    for carte in cartes:
        xml = "%s" % patron
        
        xml = set_texts(carte, xml)

        soup =  BeautifulSoup(xml, 'xml')
        
        set_color(soup, carte)
        set_lifts(soup, carte)

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

    print " == ", len(allcartes), ' cartes', len([ c for c in allcartes if c['PK'] in illustrations ]), " illustrations"
    print " == missing illustrations == \n" , "\n".join([ "%s\t%s\t%s" % (c['PK'], c['path'], c['text']) for c in allcartes if c['PK'] not in illustrations ])

    #html_table_a_img(allcartes)

main()