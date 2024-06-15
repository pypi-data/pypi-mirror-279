# Articles Graph

This example demonstrates building a graph to map out the connections between articles, sources, authors, languages, people, organization and location using the `relational` Python package.

## Installation

To set up this project, follow these steps:

1. Install the required Python packages:

```bash
pip install . 
```

2. After installing the spaCy library, download the en_core_web_sm model, if you wanna execute `articles_graph_with_nlp`:

```bash
python -m spacy download en_core_web_sm
```

## Features
- Uses [Event Registry API](https://eventregistry.org/) to get recent data
- Uses `en_core_web_sm`, which is a part of the spaCy Natural Language Processing (NLP) library to identify nodes for people, organization and location

## Files
1. `README.md` - this file
2. `daily_articles/02-04-2024.json` - the list of 100 articles for keywords technology and science
3. `articles_graph.py` - the Python script using `relationalai` package to build a graph for articles
4. `articles_graph_with_nlp.py`- the Python script using `relationalai` package to build a graph for articles and also uses natural language processing to identify entities for `Person`, `Organization` and `Location` types. 

## There are two ways to execute the script and build a graph:

### 1. Using `daily_articles/04_04_2024.json` file

- You should pass `use_local=True` for `get_articles` function. 
- You can also specify `num_articles`, the file contains 100 articles for keywords technology and science, respectively. If you run `articles_graph_with_nlp`, it is recommended to put minimum number to `num_articles`since it takes time until it proccess data via nlp.

### 2. Using [Event Registry API](https://eventregistry.org/) to get articles

- You should create free account in [Even Registry API website](https://eventregistry.org/intelligence?type=articles) and you will get 2,000 tokens for free.
- You should put your api key as `api_key` in `get_articles_request` function.
- You can also specify your own `keywords` from `KEYWORDS`list in `get_articles` function 

## Important:

if you wanna execute `articles_graph_with_nlp`, it has some prerequisites: 

1. Enable multi-valued properties by setting the compiler flag in your `raiconfig.toml` file: 

```
[compiler]
use_multi_valued = true
```
