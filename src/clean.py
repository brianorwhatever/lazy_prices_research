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

from tools import ConvertHTML, RemoveTags, RemoveNumericalTables

ticker_cik_df = pd.read_pickle('cik')
pathname_10k = '/home/jovyan/data/10k'
pathname_10q = '/home/jovyan/data/10q'

os.chdir(pathname_10k)

# Iterate over CIKs and clean HTML filings
for cik in tqdm(ticker_cik_df['cik']):
        ConvertHTML(cik)

os.chdir(pathname_10q)

# Iterate over CIKs and clean HTML filings
for cik in tqdm(ticker_cik_df['cik']):
        ConvertHTML(cik)
