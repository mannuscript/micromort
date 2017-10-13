'''
Created on Sep 8, 2017

@author: chris
'''

from bs4 import BeautifulSoup
import re
import sys
sys.path.append("./utils/")
from logger import logger

# media support: Facebook
def get_straitstimes_a2a_counts(url, html, media):
    
    a2a_counts = {}
    soup = BeautifulSoup(html, 'lxml')
    try:
        a2a_button_list = soup.findAll('a', { 'class' : ['a2abtn'] })
        for a2a_button in a2a_button_list:
            a2a_label = a2a_button.find('span', { 'class': ['a2a_label']} )
            a2a_count = a2a_button.find('span', { 'class': ['a2a_count']} )
            if a2a_label is not None and a2a_count is not None:         # It seems there are only any info for Facebook
                a2a_label_text = a2a_label.text.strip()
                a2a_count_text = a2a_count.find('span').text.strip()
                a2a_count_text = re.sub("\D","", a2a_count_text)        # To remove commas, e.g., "8,200" ==> "8200"
                a2a_counts[a2a_label_text] = int(a2a_count_text)
        return a2a_counts[media]
    except Exception as ex:
        logger.error("Failed to load count for url: " + url)
        import traceback
        traceback.print_exc()