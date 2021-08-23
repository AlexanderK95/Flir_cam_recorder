# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 16:44:00 2021

@author: Alex
"""

from pynput.keyboard import Key, Listener
from pynput import keyboard
from threading import Thread
from multiprocessing import Process

class Keylogger:
    def __init__(self):
        self.recording = False
        self.run = 1
        self.pos = 0
        
    def start(self):
        print("Start Recording by pressing SHIFT (left)")
        t = Thread(target=self.start_listener, name='keylogger', args=())
        # t = Process(target=self.start_listener, name='keylogger', args=())
        t.daemon = True
        t.start()
        return self
        
    def on_press(self,key):
        pass
    
    def on_release(self,key):
        # print('{0} release'.format(
        #     key))
        if key == Key.esc:
            # Stop listener
            print("ESC pressed! Stopping recording and saving now")
            self.recording = False
            return False
        if key == Key.shift:
            if self.recording:
                print('Recording already started! Press CTRL (left) to stop it')
            else:
                print('Start recording run %i! Press CTRL (left) to stop'%(self.run+1))
                self.run += 1
                self.recording = True
        if key == Key.ctrl_l:
            if not self.recording:
                print('No Recording running! Press SHIFT to start one')
            else:
                print('Stop recording of run %i! Press SHIFT key to start the next run or ESC to finish up'%(self.run))
                self.recording = False
        if key == Key.right:
            self.pos += 1
        if key == Key.left:
            self.pos -= 1

    def start_listener(self):
        # Collect events until released
        # listener = keyboard.Listener(
        #     on_press=self.on_press,
        #     on_release=self.on_release)
        # listener.start()
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()