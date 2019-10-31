# -*- coding: utf-8 -*-


def map(chunk):
    word_dict = {}
    for line in chunk:
        for word in line.split():
            word_dict[word] = 1
    
    return word_dict
            
                        
