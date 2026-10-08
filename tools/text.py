import re

def nettoyer_texte(chaine):
    chaine = chaine.lower()
    chaine = chaine.replace("\n", " ")
    chaine = re.sub(r"[0-9]+", " ", chaine)
    chaine = re.sub(r"[^\w\s]", " ", chaine)
    return re.sub(r"\s+", " ", chaine).strip()