import requests
import json

URL = "http://eventregistry.org/api/v1/article/getArticles"
KEYWORDS = [
    ["Municipal Bonds", "Bond", "Municipal"],
    ["Finance", "Business"],
    ["Stock", "Equity", "Share"],
    ["Technology", "Science"],
    ["Sports"],
    ["Politics"],
]

node_sizes = {
    "article": 45,
    "source": 40,
    "language": 35,
    "author": 30,
    "people": 25,
    "location": 20,
    "organization": 15,
}

node_colors = {
    "article": "blue",
    "source": "green",
    "language": "yellow",
    "author": "pink",
    "people": "cyan",
    "location": "brown",
    "organization": "purple",
}

edge_colors = {
    "publishedBy": "grey",
    "writtenIn": "purple",
    "writtenBy": "orange",
    "people": "blue",
    "location": "green",
    "organization": "red",
}


# --------------------------------------------------
# Functions to get articles
# --------------------------------------------------
def get_articles_request(keywords, num_articles):
    print("[+] Getting articles for keywords:", keywords)
    articles = []

    api_key = "YOUR_API_KEY"

    payload = {
        "action": "getArticles",
        "keyword": keywords,
        "articlesPage": 1,
        "articlesSortBy": "date",
        "articlesSortByAsc": False,
        "articlesArticleBodyLen": -1,
        "resultType": "articles",
        "isDuplicateFilter": "skipDuplicates",
        "dataType": "news",
        "apiKey": api_key,
        "forceMaxDataTimeWindow": 31,
        "articlesCount": num_articles,
    }

    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", URL, headers=headers, data=json.dumps(payload))
    try:
        articles = json.loads(response.text.encode("utf8"))
    except Exception as e:
        print("Exception occured while getting articles", e)
        return list()

    return articles["articles"]["results"]


def get_articles(num_articles=100, use_local=True, keywords=KEYWORDS[3]):
    date = "04_04_2024"
    file_name = "daily_articles/" + date + ".json"

    if not use_local:
        print(f"\tGetting articles from API for keywords: {keywords}")
        articles = list()
        for sub_keywords in keywords:
            articles += get_articles_request(sub_keywords, num_articles)
        return articles
    else:
        print(f"\tFound articles at: {file_name}")
        with open(file_name, "r") as handle:
            data_from_json = json.load(handle)
            articles = data_from_json["articles"]["results"][0:num_articles]
            return articles


##--------------------------------------------------
# Helper Functions
# --------------------------------------------------
def get_node_size_by_type(n):
    return node_sizes.get(n.get("type"), 10)


def get_node_color_by_type(n):
    return node_colors.get(n.get("type"), "red")


def get_edge_color_by_type(e):
    return edge_colors.get(e.get("type"), "black")


def get_author(article):
    authors = article.get("authors")
    if authors and isinstance(authors, list) and len(authors) > 0:
        first_author_name = authors[0].get("name", "Unknown")
    else:
        first_author_name = "Unknown Author"
    return first_author_name


def trim_node_label(label, word_limit=3):
    words = label.split()

    trimmed_label = " ".join(words[:word_limit]) + (
        "..." if len(words) > word_limit else ""
    )
    return trimmed_label
