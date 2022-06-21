# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 23:36:57 2021

@author: vargo
"""

class Person:
    ''' Quick notes/thoughts
    To create a person we need...
        * body
            ** face
            ** upper body
            ** lower body
    
    After a Person is created, we should be able to get its location
    
    With that said, the way a Person is constructed need not be formatted
    in a hierarchical matter. Instead, we check for each individual body area.
    
    Example:
        miky = Person(face=FaceObj)
        vic = Person(face = FaceObj, body = BodyObj)
    
    Note that `FaceObj`/`BodyObj` are place holders - we don't know what
    they'll be!
    The Person object then can construct the rest of the Person's body
    '''
    __init__(self, **kwargs):
        # clean_keys = [key.lower() for key in kwargs.keys()]
        clean_keys = 
        # If there's a face, make it, else, it's `None`. Same for all others.
        if "face" in clean_keys:
            self.face = clean_keys["face"]
        else:
            self.face = None
            
        if "body" in clean_keys:
            self.body = clean_keys["body"]
        else:
            self.body = None
            
        if "upper_body" in clean_keys:
            self.upper_body = clean_keys["upper_body"]
        else:
            self.upper_body = None
            
        if "lower_body" in clean_keys:
            self.lower_bodybody = clean_keys["lower_body"]
        else:
            self.lower_body = None