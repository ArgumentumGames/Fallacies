# -*- coding: utf-8 -*-

import csv


def read(path, lang):
    with open(path, 'rb') as csvfile:
        reader =  reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        rows = [ row for row in reader]

    # filters:
    #  * skip first for comments,
    #  * should have a path
    rows = rows[2:]
    rows = [ e for e in rows if len(e['path']) ]
    idx = makeidx(rows)
    
    for row in rows:
        path = row['path']
        print path
        row['depth'] = int(row['depth'])

    
        f   = path[0] 
        sf  = path[:3] if len(path) >= 3 else None
        ssf = path[:5] if len(path) >= 5 else None 

        row['f'] = f
        row['sf'] = sf
        row['ssf'] = ssf
        
        row['is_f'] = f == path
        row['is_sf'] = sf == path
        row['is_ssf'] = ssf == path
        
        #row['sfamille'] = idx[sf]['text_%s' % lang] if sf else ""
        #row['ssfamille'] = idx[ssf]['text_%s' % lang] if ssf else ""

        row['fam_num'] = "%s" % f
        row['fam_text'] = idx[f]['text_%s' % lang]

        text = row['text_%s' % lang]
        row['text'] = text.strip('\n')
        row['txt1'] = text.split('\n')[0]
        row['txt2'] = ("%s\n" % text).split('\n')[1]
        
        row['desc'] = row['desc_%s' % lang]
        row['example'] = row['example_%s' % lang]
        row['link'] = row['link_%s' % lang]
        row['color']= idx['%s'% f]['svg_color']
        
        for xj in xrange(1,4):
            row["sfam_%s"%xj] = idx["%s.%s" % (f, xj)]['text_%s' % lang]

        if row['depth'] >= 2:
            for xj in xrange(1,4):
                row["ssfam_%s"%xj] = idx["%s.%s" % ( row['sf'], xj)]['text_%s' % lang]
            
    return rows

def makeidx(rows):
    return { e['path']: e  for e in rows }

def add_rels(rows):
    idx = makeidx(rows)
    for e in rows:
        parent = e['path'][:-2] if not e['is_f'] else '0'
        rels = list(set(filter( lambda e : e is not None, [
            e['f'] if e['is_f'] else None,
            e['sf'] if e['is_sf'] else None,
            e['ssf'] if e['is_ssf'] else None,
            parent,
            e.get("""
                    =================================
                    !!!!!    EDGE TRANSVERSE    !!!!!!
                    =================================
            """, None)
        ])))
        
        e['rels'] = rels
        
    return rels
        
def get_cartes(rows):
    cartes = filter( lambda e : len(e['carte']), rows )
    return cartes


def main():
    path = "../csv/argumentum.csv"
    rows = read(path, lang)
    cartes = get_cartes(rows)

    keys = ['path', 'depth', 'text_%s' % lang, 'link_%s' % lang, 'example_%s' % lang, 'famille', 'sfamille', 'ssfamille', 'desc_fr', 'svg_color',  'svg_illustration', ]
    #for r in cartes :
        #print ' '.join( map( lambda e: r[e], keys ) )



