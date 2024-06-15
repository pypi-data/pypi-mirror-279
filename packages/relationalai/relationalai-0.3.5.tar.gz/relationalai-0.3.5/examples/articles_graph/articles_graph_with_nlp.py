import warnings
import utils
import en_core_web_sm
import requests

import relationalai as rai
from relationalai.std.graphs import Graph

nlp = en_core_web_sm.load()
warnings.filterwarnings("ignore")


def check_wiki_page(query):
    try:
        result = requests.get(f"https://en.wikipedia.org/wiki/{query}", verify=False)
    except Exception:
        pass

    if result.status_code == 200:
        return True
    return False


# --------------------------------------------------
# Load data
# --------------------------------------------------
articles = utils.get_articles(num_articles=20, use_local=True)

# --------------------------------------------------
# Types
# --------------------------------------------------
model = rai.Model("ArticleAnalysis")
Article = model.Type("Article")
ContentSource = model.Type("ContentSource")
Language = model.Type("Language")
Author = model.Type("Author")
People = model.Type("People")
Location = model.Type("Location")
Organization = model.Type("Organization")

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

        # get the nlp data for the article body
        text_nlp = nlp(article["body"])
        print("Processing entities in the articles using NLP...")

        # iterates over each entity recognized in the article.
        for ent in text_nlp.ents:
            print("Entity:", ent.text, "Label:", ent.label_)

            # explicitly skip entities containing the "%" symbol to prevent processing of numerical or statistical data, 
            # assuming such entities are less relevant to our context
            if "%" in ent.text:
                continue

            ent_text = ent.text.lower().replace("-", "").replace("'s", "")

            # checks if there's a Wikipedia page for the entity text. If not, the entity is skipped, using this as a criterion for notability and relevance.
            if not check_wiki_page(ent_text):
                continue

            # adds the entity to the Organization type and sets it as the organization of the article
            # if it's recognized as an organization.
            if ent.label_ == "ORG":
                organization = Organization.add(name=ent_text)
                a.organizations.add(organization)
            # adds the entity to the People type and sets it as the people of the article
            # if it's recognized as a person.
            elif ent.label_ == "PERSON":
                people = People.add(name=ent_text)
                a.peoples.add(people)
            # adds the entity to the Location type and sets it as the location of the article
            elif ent.label_ == "GPE":
                location = Location.add(name=ent_text)
                a.locations.add(location)

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

    Node.add(a.peoples, label=a.peoples.name, type="people")
    Node.add(a.locations, label=a.locations.name, type="location")
    Node.add(a.organizations, label=a.organizations.name, type="organization")

    Edge.add(a, a.source, type="publishedBy")
    Edge.add(a, a.language, type="writtenIn")
    Edge.add(a, a.author, type="writtenBy")

    Edge.add(a, a.peoples, type="people")
    Edge.add(a, a.locations, type="location")
    Edge.add(a, a.organizations, type="organization")

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
