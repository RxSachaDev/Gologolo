import urllib.request
import xmltodict
from datetime import datetime
from Document import DocumentFactory


def collect_arxiv_posts(taille_docs: int, theme: str):

    url = f"http://export.arxiv.org/api/query?search_query=all:{theme}&start=0&max_results={str(taille_docs)}"

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

    # Listes contenant les textes
    docs = []

    for entry in entries:
        title = entry['title'].replace('\n', ' ').strip()
        # Gérer les cas de liste ou non 
        if isinstance(entry['author'], list):
            authors = [author['name'] for author in entry['author']]
        else:
            authors = [entry['author']['name']]
        date = datetime.fromisoformat(entry['published'].replace('Z', '+00:00'))
        url = entry['id']
        text = entry['summary'].replace('\n', ' ').strip()

        docs.append(
            DocumentFactory.create_document(
                source="Arxiv",
                title = title,
                author = authors[0],
                date = date,
                url = url,
                text = text,
                coauthors = authors[1:]
            )
        )

    return docs