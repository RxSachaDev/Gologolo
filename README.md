# Gologolo

Gologolo est un moteur de recherche simple sur un corpus d'articles Reddit et
d'Arxiv. Il récupère les documents, les sauvegarde dans `corpus.csv`, puis
permet de les rechercher avec un classement TF-IDF. Une interface interactive
est fournie dans le notebook `recherche.ipynb`.

## Dépôt et versions

Le code source et les fichiers nécessaires sont disponibles sur
[GitHub : RxSachaDev/Gologolo](https://github.com/RxSachaDev/Gologolo).

Les étapes du projet sont repérées par les tags Git :

- `v1` : socle de base (première partie) ;
- `v2` : socle et moteur de recherche (deux premières parties) ;
- `v3` : projet complet avec interface (troisième partie).

Pour récupérer une version précise, remplacer `v3` par le tag souhaité :

```powershell
git checkout v3
```

## Prérequis

- Python 3.13 ;
- un compte Reddit et des identifiants d'application Reddit pour collecter les
  publications Reddit ;
- VS Code avec l'extension Jupyter pour utiliser l'interface du notebook.

Les dépendances Python sont listées dans [`requirements.txt`](requirements.txt).

## Installation

Depuis la racine du dépôt, sous PowerShell :

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Créez un fichier `.env` à la racine du projet à partir de
[`.env.example`](.env.example) et renseignez les identifiants Reddit. Ce fichier
contient des secrets et ne doit pas être commité.

```powershell
Copy-Item .env.example .env
```

```dotenv
REDDIT_CLIENT_ID=votre_client_id
REDDIT_CLIENT_SECRET=votre_client_secret
REDDIT_USER_AGENT=Gologolo/1.0 par u/votre_nom_utilisateur
```

## Exécution

La première exécution collecte les publications du thème configuré dans
`main.py` depuis Reddit et Arxiv, puis crée `corpus.csv` :

```powershell
python main.py
```

Le programme demande ensuite un nom d'auteur et des mots-clés. Les exécutions
suivantes réutilisent le corpus sauvegardé. Pour ouvrir l'interface, ouvrez
`recherche.ipynb` dans VS Code, sélectionnez l'environnement `.venv`, puis
exécutez les cellules. Le notebook utilise le fichier `corpus.csv` créé par
`main.py`.

`corpus.csv` et `.env` sont des fichiers locaux ignorés par Git ; le corpus
est régénéré sur la machine de l'utilisateur.
