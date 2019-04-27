import subprocess
import json
import sys
sys.path.append('../..') 

sets = {
    "max_width":  1500,
    "max_height": 1500,    
    "style": "magnificent",
    "angle_tolerance": 0,
    "position":"center"
}

def svg_to_paths(file_name):
    p=subprocess.call(['/usr/bin/inkscape','{file_path} --verb EditSelectAll --verb SelectionUngroup --verb ObjectToPath --verb FileQuit'])

def svg_to_points(settings: dict):
    with open('svg_to_points/svg_to_points.linux-arm64/data/settings.json','w') as file:
        json.dump(settings, file)
    p=subprocess.call(['bash', 'svg_to_points/svg_to_points.linux-arm64/svg_to_points'])
    
    with open('svg_to_points/svg_to_points.linux-arm64/data/result.json') as file:
        print(json.load(file))

if __name__ == "__main__":
    svg_to_points(sets)