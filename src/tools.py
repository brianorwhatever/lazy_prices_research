
# Importing built-in libraries (no need to install these)
import re
import os
from time import gmtime, strftime
from datetime import datetime, timedelta
import unicodedata

# Importing libraries you need to install
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import bs4 as bs
from lxml import html
from tqdm import tqdm


def RemoveNumericalTables(soup):
    
    '''
    Removes tables with >15% numerical characters.
    
    Parameters
    ----------
    soup : BeautifulSoup object
        Parsed result from BeautifulSoup.
        
    Returns
    -------
    soup : BeautifulSoup object
        Parsed result from BeautifulSoup
        with numerical tables removed.
        
    '''
    
    # Determines percentage of numerical characters
    # in a table
    def GetDigitPercentage(tablestring):
        if len(tablestring)>0.0:
            numbers = sum([char.isdigit() for char in tablestring])
            length = len(tablestring)
            return numbers/length
        else:
            return 1

    # Evaluates numerical character % for each table
    # and removes the table if the percentage is > 15%
    [x.extract() for x in soup.find_all('table') if GetDigitPercentage(x.get_text())>0.15]
    return soup

def RemoveTags(soup):
    
    '''
    Drops HTML tags, newlines and unicode text from
    filing text.
    
    Parameters
    ----------
    soup : BeautifulSoup object
        Parsed result from BeautifulSoup.
        
    Returns
    -------
    text : str
        Filing text.
        
    '''
    
    # Remove HTML tags with get_text
    text = soup.get_text()
    
    # Remove newline characters
    text = text.replace('\n', ' ')
    
    # Replace unicode characters with their
    # "normal" representations
    text = unicodedata.normalize('NFKD', text)
    
    return text

def ConvertHTML(cik):
    
    '''
    Removes numerical tables, HTML tags,
    newlines, unicode text, and XBRL tables.
    
    Parameters
    ----------
    cik : str
        Central Index Key used to scrape files.
    
    Returns
    -------
    None.
    
    '''
    
    # Look for files scraped for that CIK
    try: 
        os.chdir(cik)
    # ...if we didn't scrape any files for that CIK, exit
    except FileNotFoundError:
        print("Could not find directory for CIK", cik)
        return
        
    print("Parsing CIK %s..." % cik)
    parsed = False # flag to tell if we've parsed anything
    
    # Try to make a new directory within the CIK directory
    # to store the text representations of the filings
    try:
        os.mkdir('rawtext')
    # If it already exists, continue
    # We can't exit at this point because we might be
    # partially through parsing text files, so we need to continue
    except OSError:
        pass
    
    # Get list of scraped files
    # excluding hidden files and directories
    file_list = [fname for fname in os.listdir() if not (fname.startswith('.') | os.path.isdir(fname))]
    
    # Iterate over scraped files and clean
    for filename in file_list:
            
        # Check if file has already been cleaned
        new_filename = filename.replace('.html', '.txt')
        text_file_list = os.listdir('rawtext')
        if new_filename in text_file_list:
            continue
        
        # If it hasn't been cleaned already, keep going...
        
        # Clean file
        with open(filename, 'r') as file:
            parsed = True
            soup = bs.BeautifulSoup(file.read(), "lxml")
            soup = RemoveNumericalTables(soup)
            text = RemoveTags(soup)
            with open('rawtext/'+new_filename, 'w') as newfile:
                newfile.write(text)
    
    # If all files in the CIK directory have been parsed
    # then log that
    if parsed==False:
        print("Already parsed CIK", cik)
    
    os.chdir('..')
    return
