'''It is vk chat bot client module for project christina'''
import sys
sys.path.append('../../..')
import argparse
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randint
import json
from christina_reborn.common.logger import Logger

Logger.def_logger_file()
log = Logger.get_logger_by_name(__name__)

message_tree_template = {
    'answer':'This is christine vk control panel alpha 0.1.',
    'wrong':None,
    'function': None,
    'next':{
        'tasks':{
            'answer':'Table of current tasks:',
            'wrong':'Wrong command. Write "help" to get information',
            'function':'func',
            'next':None
            },
        'write':{
            'answer':'Task added.',
            'wrong':None,
            'function':'write',
            'next':None
            },
        'upload':{
            'answer':'Ready to recieve an svg file. Write "upload" again and attach svg file to message.',
            'wrong':'Write "upload" again and attach svg file to message or write help to get information.',
            'function':None,
            'next':{
                'upload':{
                'answer':'Image is being uploaded... ',
                'function':'upload',
                'next':None
                }
            }
        }
    }
}

no_condition_answers_template = {
    'back':{
            'answer':'Going back to initial screen...',
            'function':'back',
            },
    'about':{
            'answer':'ans1',
            'function':'about',
            },
    'help':{
            'answer':None,
            'function':'help',
            }
} 

help_message = 'This is christine vk control panel alpha 0.1.\n\
                Following commands are available:\n\
                Upload - allows to upload an svg file to device\n\
                Tasks - get list of current tasks\n\
                Back - go to initial screen\n\
                About - read few words about author\n\
                Help - show this message'

about_message = 'Author of this brilliant masterpiece is FF220v.\n\
                Current version: 0.1 alpha\n\
                Dedicated to those who like robots and pythons'

wrong_default = 'Wrong command. Write "help" to get information'

class MainDialog():
    '''Main class which is used to interract with users
    (1 instance per user id), it is constructed in a way to
    provide following features:
    - Using common dialog tree to interract with users
    - Evaluate functions mentioned in dialog tree
    (functions must be members of this class and take
    one string as an arguement)'''
    

    def __init__(self, vk_session, user_id):
        self.no_condition_answers = no_condition_answers_template
        self.initial_tree = message_tree_template
        self.current_tree = self.initial_tree
        self.previous_tree = self.current_tree 
        self.user_id = user_id
        self.vk_session = vk_session
        self.api = vk_session.get_api()
        self.current_event = None
    '''Here are user functions'''

    def upload(self,msg):
        print(self.current_event.attachments)

    def back(self,msg):
        self.set_tree(self.initial_tree)
        self.send_text(self.current_tree['answer'])

    def write(self,msg):
        self.send_text('I am so sad about this, but the server does not exist yet,\n\
            so where is no place I can send your text(((')        

    def about(self,msg):
        self.send_text(about_message)

    def help(self,msg):
        self.send_text(help_message)

    def func(self,msg):
        print('hello')

    '''Here go technical functions'''
    
    def send_text(self, msg):
        self.api.messages.send(user_id = self.user_id, message = msg, random_id = randint(0,0xFFFFFFFF))
    
    def set_tree(self, tree):
        self.previous_tree = self.current_tree
        self.current_tree = tree

    def handle_function(self,func_str, msg):
        eval('self.' + func_str + '(\''+msg+'\')')

    def check_msgs(self, event):
        self.current_event = event
        msg = event.text
        try:
            msg_cmd = msg.split()[0].lower()
        except:
            msg_cmd = ' '
        if msg_cmd in self.no_condition_answers:
            if self.no_condition_answers[msg_cmd]['answer'] != None:
                self.send_text(self.no_condition_answers[msg_cmd]['answer'])
            if self.no_condition_answers[msg_cmd]['function'] != None:
                self.handle_function(self.no_condition_answers[msg_cmd]['function'],msg)            
        else:
            if msg_cmd in self.current_tree['next']:
                self.set_tree(self.current_tree['next'][msg_cmd])
                if self.current_tree['answer'] != None:
                    self.send_text(self.current_tree['answer'])
                if self.current_tree['function'] != None:
                    self.handle_function(self.current_tree['function'],msg)
                if self.current_tree['next'] == None:
                    self.set_tree(self.initial_tree)
                    self.send_text(self.current_tree['answer'])
            else:
                if self.current_tree['wrong'] != None:
                    self.send_text(self.current_tree['wrong'])    
                else:
                    self.send_text(wrong_default)    


if __name__ == '__main__':
    
    with open('auth_data.json') as f:
        auth_data = json.load(f)
    
    vk_session = vk_api.VkApi(token=auth_data['token'])

    log.info('Creating longpoll...')
    longpoll = VkLongPoll(vk_session)
    log.info('Longpoll created. Listening...')
    dialog_dict = {}
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user_id = event.user_id
                log.info('Incoming message from '+str(user_id)+': '+event.text)    
                if user_id not in dialog_dict:
                    dialog_dict[user_id] = MainDialog(vk_session = vk_session, user_id = user_id)
                dialog_dict[user_id].check_msgs(event)