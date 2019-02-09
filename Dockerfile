FROM jupyter/datascience-notebook:latest

RUN pip install lxml tqdm

ADD src .

ADD cik .

ADD lazy_prices_scraping.ipynb .

CMD ["python3", "clean.py"]
