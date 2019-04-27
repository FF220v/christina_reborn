import subprocess
import json
import sys
sys.path.append('../..') 
from common.logger import Logger
"""
settings_example = {
    "max_width":  1500,
    "max_height": 1500,    
    "style": "magnificent",
    "angle_tolerance": 0,
    "position":"center"
    "make_paths":False
    "path":"./file.svg"
}
"""

validation_list = ['max_width','max_height','style','angle_tolerance','position','make_paths','path']

def svg_to_paths(file_name):
    p=subprocess.call(['/usr/bin/inkscape','{file_path} --verb EditSelectAll --verb SelectionUngroup --verb ObjectToPath --verb FileQuit'])

def svg_to_points(settings: dict):
    log = get_logger_by_name(__name__)
    log.info('Validating settings...')
    valid = True
    for key in validation_list:
        if key not in settings:
            valid = False
            log.error('key {key} should be in settings'.format(key = key))
    if valid:    
        with open('svg_to_points/svg_to_points.linux-arm64/data/settings.json','w') as file:
            json.dump(settings, file)
        p=subprocess.call(['bash', 'svg_to_points/svg_to_points.linux-arm64/svg_to_points'])
        
        with open('svg_to_points/svg_to_points.linux-arm64/data/result.json') as file:
            print(json.load(file))
        return 0
    else:
        return -1
if __name__ == "__main__":
    svg_to_points(sets)