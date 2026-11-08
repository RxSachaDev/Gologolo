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
REDDIT_USER_AGENT=u/votre_nom_utilisateur
```

## Exécution

Utilisez le fichier `corpus.csv` fourni dans le dernier commit du dépôt. Après
avoir récupéré les dernières modifications (`git pull` sur la branche `main`),
conservez ce fichier : `main.py` et le notebook `recherche.ipynb` le chargent
directement.

Si `corpus.csv` est absent, `main.py` collecte les publications du thème
configuré dans le code depuis Reddit et Arxiv, puis crée le fichier :

```powershell
python main.py
```

Le programme demande ensuite un nom d'auteur et des mots-clés. Les exécutions
suivantes réutilisent le corpus sauvegardé. Pour ouvrir l'interface, ouvrez
`recherche.ipynb` dans VS Code, sélectionnez l'environnement `.venv`, puis
exécutez les cellules.

Le fichier `.env` est local et ignoré par Git. `corpus.csv` est versionné dans
le dépôt ; ne le remplacez pas par une ancienne copie si vous devez utiliser le
corpus du dernier commit.
