# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 00:11:42 2018

@author: Sam
"""
import wikipedia
from collections import Counter
from nltk import word_tokenize
import string
from numpy.random import choice
import json

table = str.maketrans(dict.fromkeys(string.punctuation))
def strip_punctuation_and_make_lower(text): 
    return text.translate(table).lower()

def tokenize(text): 
    return word_tokenize(strip_punctuation_and_make_lower(text))

class WikipediaWordCounter:
    
    def __init__(self, seed_term, depth = 3, num_links = 5): 
        self.depth = depth
        self.seed_term = seed_term
        self.scraped_pages = set() 
        self.num_links = num_links
        self.word_counts = Counter()
        
    def _add_to_word_counts(self, content): 
        self.word_counts.update(tokenize(content))
        
    def run(self):
        self._count_page(self.seed_term, 0)
        
    def _count_page(self, curr_page_name, curr_depth):
        if curr_depth >= self.depth: 
            return 
        elif curr_page_name in self.scraped_pages:
            return
        else:
            self.scraped_pages.add(curr_page_name)
            try:
                curr_page = wikipedia.page(curr_page_name)
            except: 
                print("error scraping", curr_page_name)
                return 
            print("scraping", curr_page_name)
            self._add_to_word_counts(curr_page.content) 
            for page_name in choice(curr_page.links,size=self.num_links,replace=False): 
                self._count_page(page_name, curr_depth + 1) 
    
    def get_wc(self): 
        return self.word_counts
    
    def save(self, filename = "wwc.json"): 
        save_data = {"meta":{"scraped_pages":list(self.scraped_pages), 
                                 "seed_term":self.seed_term},
                     "data":self.word_counts}
        
        with open(filename,'w') as outfile: 
            json.dump(save_data, outfile, indent=1)

if __name__ == "__main__": 
    ws = WikipediaWordCounter("New York City", num_links=2) 
    ws.run()
    ws.save()