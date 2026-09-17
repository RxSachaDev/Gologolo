import urllib.request
import xmltodict
import pandas as pd


def collect_arxiv_posts(taille_docs: int):

    url = "http://export.arxiv.org/api/query?search_query=all:tennis&start=0&max_results=" + str(taille_docs)

    # Requête avec User-Agent
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

    # Récupération des données XML
    with urllib.request.urlopen(req) as response:
        xml_data = response.read().decode('utf-8')

    # Conversion XML -> dictionnaire Python
    parsed = xmltodict.parse(xml_data)

    # Récupération des articles
    entries = parsed['feed'].get('entry', [])

    # S'il n'y a qu'un seul article
    if isinstance(entries, dict):
        entries = [entries]

    print("Nombre d'articles ArXiv trouvés :", len(entries))

    # Listes contenant les textes et leur origine
    docs = []
    origins = []

    for entry in entries:
        texte = entry['summary'].replace('\n', ' ').strip()

        docs.append(texte)
        origins.append("arxiv")

    return docs, origins