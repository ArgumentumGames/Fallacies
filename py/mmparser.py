
from pprint import pprint
from collections import Iterable, defaultdict

def etree_to_dict(t):
    """ http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree#7684581 """
    tag = t.tag.lower()
    d = {tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k.lower()].append(v)
        d = {tag: {k.lower():v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[tag].update((k.lower(), v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d



def simplenode(el, key):
    #print el
    root = key == ""
    family = len(key) == 1
    
    children = []
    
    if 'node' in el:
        if type(el['node']) == list:
            for i,e in enumerate(el['node']):
                children.append(simplenode(e, "%s%s%s" % (key, "." if len(key) else "" ,  i+1) ))
        else : 
            children = [simplenode(el['node'], "%s.%s" % (key, 1) )]

    if root : shape = "diamond"
    elif family : shape = "square"
    else : shape = "circle"

    return { 'id' : el.get('id', ""),
             'key' : 'root' if root else key,
             'parent' : '',
             'shape' : shape,
             'text_fr' : el.get('text', ""),
             'link_fr' : el.get('link', ""),
             'text_en' : "",
             'link_en' : "",
             'children' : children ,
             'edge'  : el.get('edge',  {}),
             'arrow' : el.get('arrowlink', {}) 
           }


def flatten(x):

    array = []
    def _flat(d):
        if type(d) == dict :
            array.append( d )
            e = d.get("children", [])
            for el in e:
                el['parent'] = d['key']
                if len(el):
                    for sub in _flat(el):
                        #print el, sub
                        if len(sub):
                            yield sub
                else:
                    yield el
            else:
                yield e

    list(_flat(x))
    
    return array


#
# : key ; titre_FR ; titre_EN ; descri_FR ; descri_EN ; Exemple_FR ; Exemple_EN ; Nom Latin ; Dicton_proverbe ; image ; carte[bool]; lien_http_FR ; lien_http_EN;


        
def main(src, cmd):
    from xml.etree import cElementTree as ET
    
    source = "<?xml version=\"1.0\"?>" + open(src).read()
    e = ET.XML(source)

    d = etree_to_dict(e)['map']['node']
    d = simplenode(d, "")
    
    flat = [ e for e in flatten(d) ]
    #flat = filter(lambda e: len(e['key']) , flat)

    byid  = { e['id']: e for e in flat }
    bykey  = { e['key']: e for e in flat }

    
    for e in flat:
        root = e['key'] == 'root'
        k = e['key'].split(".")[0]
        e['label'] = e['text_fr'] 
        
        e['family'] = bykey[k]['text_fr']
        e['rel'] = byid[ e['arrow']['destination']]['key'] if 'destination' in e['arrow'] else ""
        k = e['rel'].split(".")[0]
        e['rel_family'] = bykey[k]['text_fr'] if len(e['rel']) else ""

        k = e['key'].split(".")
        if root : e['path'] = "/"
        else : e['path'] = u"/".join( [ bykey[".".join(k[:i+1])]['text_fr'] for i, _ in enumerate(k) ])
        #else : e['path'] = [ i for i, _ in enumerate(k) ]
        
    # Nodes
    if cmd == "-n":
        separator = ","
        columns = """
        key
        carte
        shape
        image
        text_fr
        text_en
        desc_fr
        desc_en
        example_fr
        example_en
        latin
        proverbe
        link_fr
        link_en
        """.split()

        print "%s\n" % ( separator.join(columns) )
        print ( tocsv(flat, columns, separator).encode('utf8') )

    # Edges
    if cmd == "-e":
        flat = [ e for e in flat if len(e['children']) == 0 ]
        def iteredges():
            for e in flat:
                key = e['key'].split('.')
                for v in ( "%s -- %s" % (".".join(key[:i]), ".".join(key[:i+1]) )
                    for i, _ in enumerate(key) if i > 0 ):
                    yield v 

        csv = sorted(list(set(iteredges())))
        print ( "\n".join(csv).encode('utf8') )
        

    # Edges transfamily
    if cmd == "-t":
        
        _ = lambda e : "{key} -- {rel}".format(**e)
        #_ = lambda e : "  ".join(e.keys())
        csv = [ _(e) for e in flat if len(e['rel']) ]
        
        print ( "\n".join(csv).encode('utf8') )
    
def tocsv(flat, cols, separator):
    _ = lambda e : [ e.get(k, "") for k in cols ]
    csv = [ separator.join(_(e)) for e in flat ]
    return "\n".join(csv)

    
if __name__ == "__main__":
    import sys
    main("../fallacies.mm", sys.argv[1])