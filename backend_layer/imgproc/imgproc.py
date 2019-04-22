from six import StringIO
import xml.etree.ElementTree as etree
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import requests
from svgpath2mpl import parse_path
from matplotlib.path import Path

def svg2points(svg):
    tree = etree.parse(StringIO(r.text))
    root = tree.getroot()
    path_elems = root.findall('.//{http://www.w3.org/2000/svg}path')

    paths = [parse_path(elem.attrib['d']) for elem in path_elems]

    poly = []
    for path in paths:
        poly.append(path.to_polygons(closed_only = False))

    return poly

if __name__ == "__main__":
    r = requests.get('https://psv4.userapi.com/c834500/u94734732/docs/d6/d05c77fd3769/yoba.svg?extra=9T6ccsa2hadnVedfX9ObhD7F-gaNOuw0DYqnaZN_Krtqgue2OM5XgeVjXwLEGot0un62GsNjqzqCISfpcaVpyU-EJq9_YfnhQ-pz3PlUPdsLJ9IlMY86R70tgR1bnc2dqqa69o5YCpTjCGRTFYwA&dl=1')

    poly = svg2points(r)

    fig = plt.figure(figsize=(10,10))
    print(poly)
    print(len(poly))
    for p in poly:
        print(len(p))
        for k in p:
            print(len(k))
            for y in k:
                plt.plot(y[0],y[1], marker = 'o')
    plt.show()
    