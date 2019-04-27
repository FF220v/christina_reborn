from six import StringIO
import xml.etree.ElementTree as etree
import matplotlib.pyplot as plt
from matplotlib.transforms import TransformedBbox
import requests
from svgpath2mpl import parse_path
import subprocess

def svg2paths(file_name):
    p=subprocess.call(['/usr/bin/inkscape','file1.svg','file2.pdf'])

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
    r = requests.get('https://psv4.userapi.com/c848228/u94734732/docs/d16/9699224cd9d3/drawing-1.svg?extra=Kvk60XH5r-RCVwYEuIrl9rCUj0AlCVM3IzpR1JxgjjSZvve6uLJMJ5BVDQZhtU6xLTDUbVkaziDTIesS7-NJsnVw42dAk3JUy--__OuzdhjmDM7Er2G9tpS4OIhyPVjIpSa7z-0tFFZX15cJBp7V&dl=1')

    poly = svg2points(r)

    fig = plt.figure(figsize=(10,10))
    points = 0
    for p in poly:
        for k in p:
            for y in k:
                points += 1
                print(points) 
                plt.plot(y[0],y[1], marker = 'o')
    print('Points total: {p}'.format(p=points))
    plt.show()
    