import subprocess
import json
import sys
sys.path.append('../..') 

def svg_to_paths(file_name):
    p=subprocess.call(['/usr/bin/inkscape','{file_path} --verb EditSelectAll --verb SelectionUngroup --verb ObjectToPath --verb FileQuit'])

def svg_to_points(settings: dict):
    with open('svg_to_points/svg_to_points.linux-arm64/data/settings.json','w') as file:
        json.dump(file, settings)
    p=subprocess.call(['bash', 'svg_to_points/svg_to_points.linux-arm64/svg_to_points'])
    
    with open('svg_to_points/svg_to_points.linux-arm64/data/result.json','w') as file:
        print(json.load(file))
    