import utils

import relationalai as rai
from relationalai.std.graphs import Graph

# --------------------------------------------------
# Load data
# --------------------------------------------------
articles = utils.get_articles(num_articles=5, use_local=True)

# --------------------------------------------------
# Types
# --------------------------------------------------
model = rai.Model("ArticleAnalysis")
Article = model.Type("Article")
ContentSource = model.Type("ContentSource")
Language = model.Type("Language")
Author = model.Type("Author")

# --------------------------------------------------
# Load data
# --------------------------------------------------
with model.rule(dynamic=True):
    for article in articles:
        source = ContentSource.add(name=article["source"]["title"])
        language = Language.add(name=article["lang"])
        author = Author.add(name=utils.get_author(article))

        a = Article.add(
            title=article.get("title", "Unknown Title"),
            trimmed_title=utils.trim_node_label(article.get("title", "Unknown Title")),
            sentiment=article["sentiment"] or "N/A",
            body=article["body"],
            dType=article["dataType"],
            published_on=article["dateTimePub"],
            date=article["date"],
            url=article["url"],
            language=language,
            author=author,
            source=source,
        )

# --------------------------------------------------
# Query for articles to see what we have
# --------------------------------------------------
with model.query() as select:
    a = Article()
    response = select(a.title, a.body, a.date, a.source)
print(response.results)

# --------------------------------------------------
# Graph
# --------------------------------------------------
graph = Graph(model)
Node, Edge = graph.Node, graph.Edge

with model.rule():
    a = Article()
    Node.add(a, label=a.trimmed_title, type="article")
    Node.add(a.source, label=a.source.name, type="source")
    Node.add(a.language, label=a.language.name, type="language")
    Node.add(a.author, label=a.author.name, type="author")
    Edge.add(a, a.source, type="publishedBy")
    Edge.add(a, a.language, type="writtenIn")
    Edge.add(a, a.author, type="writtenBy")

graph.visualize(
    three=False,
    show_edge_label=True,
    node_label_size_factor=1.5,
    node_size_factor=1.5,
    node_hover_neighborhood=True,
    show_node_label=True,
    style={
        "node": {
            "size": utils.get_node_size_by_type,
            "color": utils.get_node_color_by_type,
        },
        "edge": {
            "opacity": 0.8,
            "color": utils.get_edge_color_by_type,
            "label": lambda t: f'{t["type"]}',
        },
    },
).display()
