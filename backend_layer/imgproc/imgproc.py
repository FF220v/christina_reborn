import subprocess
import json
import sys
import os
sys.path.append('../..')
import shutil
from common.logger import Logger
INKSCAPE_TIMEOUT = 20
settings_example = {
    "max_width":  100,
    "max_height": 100,    
    "style": "magnificent",
    "angle_tolerance": 0,
    "position":"center",
    "make_paths":True,
    "path":"/backend_layer/imgproc/test.svg"
}

log = Logger.get_logger_by_name(__name__)
os.chdir('../..')

validation_list = ['max_width','max_height','style','angle_tolerance','position','make_paths','path']

def svg_to_paths(file_path):
    log.info('Converting all contours to paths...')
    try:
        log.info('Calling inkscape...')
        p=subprocess.call('inkscape -f ' + os.getcwd() + file_path + ' --verb EditSelectAll --verb SelectionUnGroup --verb EditSelectAll --verb ObjectToPath --verb FileSave --verb FileQuit', shell = True, timeout = INKSCAPE_TIMEOUT)    
        log.info('Points converted to paths')
    except: 
        log.error('Timeout expired')    

def svg_to_points(settings: dict):
    log.info('Validating settings...')
    valid = True
    for key in validation_list:
        if key not in settings:
            valid = False
            log.error('key {key} should be in settings'.format(key = key))
    if valid:
        log.info('Settings valid')
        log.info('Making work copy /backend_layer/imgproc/svg_to_points/svg_to_points.linux-arm64/data/file_to_convert.svg')
        shutil.copy2(os.getcwd() + settings['path'], os.getcwd() + '/backend_layer/imgproc/svg_to_points/svg_to_points.linux-arm64/data/file_to_convert.svg') 
        if settings['make_paths']:
            svg_to_paths('/backend_layer/imgproc/svg_to_points/svg_to_points.linux-arm64/data/file_to_convert.svg')     

        with open('backend_layer/imgproc/svg_to_points/svg_to_points.linux-arm64/data/settings.json','w') as file:
            json.dump(settings, file)
        log.info('Calling java app svg_to_points...')
        p=subprocess.call(['bash', 'backend_layer/imgproc/svg_to_points/svg_to_points.linux-arm64/svg_to_points'])
        
        with open('backend_layer/imgproc/svg_to_points/svg_to_points.linux-arm64/data/result.json') as file:
            print(json.load(file))
        shutil.copy2(os.getcwd() + '/backend_layer/imgproc/svg_to_points/svg_to_points.linux-arm64/data/result.json',os.getcwd() + settings['path'][:len(settings['path'])-3]+'json')
    else:
        log.error('Invalid settings. Cannot perform operation')

if __name__ == "__main__":
    svg_to_points(settings_example)