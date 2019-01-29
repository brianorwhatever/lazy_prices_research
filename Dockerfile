FROM jupyter/datascience-notebook:latest

RUN pip install lxml tqdm

ADD cik .
ADD lazy_prices_scraping.ipynb .
