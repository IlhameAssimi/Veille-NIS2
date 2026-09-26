import urllib.request
import xml.etree.ElementTree as ET
import re

# Nettoie le HTML du résumé pour avoir un texte propre dans le tableau
def clean_html(raw_html):
    clean_text = re.sub(r'<[^>]+>', '', raw_html)
    clean_text = clean_text.replace('\n', ' ').replace('|', '-').strip()
    return clean_text[:120] + "..." if len(clean_text) > 120 else clean_text

# Liste de 11 sources officielles et certifiées (Cybersécurité, NIS 2, DevSecOps)
SOURCES = [
    # 1. Sources Gouvernementales et Officielles Françaises
    {"nom": "CERT-FR (Alertes)", "url": "https://www.cert.ssi.gouv.fr/alerte/feed/"},
    {"nom": "CERT-FR (Avis)", "url": "https://www.cert.ssi.gouv.fr/avis/feed/"},
    {"nom": "CNIL", "url": "https://www.cnil.fr/fr/rss.xml"},
    {"nom": "Cybermalveillance.gouv.fr", "url": "https://www.cybermalveillance.gouv.fr/feed"},
    
    # 2. Organismes Européens (Origine de NIS 2)
    {"nom": "ENISA (Europe)", "url": "https://www.enisa.europa.eu/news/enisa-news/RSS"},
    
    # 3. Médias Spécialisés IT & Cybersécurité
    {"nom": "Le Monde Informatique", "url": "https://www.lemondeinformatique.fr/flux-rss/thematique/securite/rss.xml"},
    {"nom": "ZDNet France (Sécurité)", "url": "https://www.zdnet.fr/feeds/rss/actualites/securite/"},
    {"nom": "L'Informaticien", "url": "https://www.linformaticien.com/rss.xml"},
    {"nom": "Usine Digitale (Cyber)", "url": "https://www.usine-digitale.fr/securite-informatique/rss"},
    
    # 4. Veille Technique & DevSecOps
    {"nom": "Zinetis (Cyber)", "url": "https://www.zinetis.com/feed/"},
    {"nom": "BleepingComputer", "url": "https://www.bleepingcomputer.com/feed/"}
]

articles = []
for source in SOURCES:
    try:
        req = urllib.request.Request(
            source["url"], 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        xml_data = urllib.request.urlopen(req, timeout=5).read()
        root = ET.fromstring(xml_data)

        for item in root.findall('.//item')[:1]:
            title = item.find('title').text.replace('|', '-').strip()
            link = item.find('link').text.strip()
            
            # Récupération et nettoyage du résumé
            desc_node = item.find('description')
            summary = clean_html(desc_node.text) if desc_node is not None and desc_node.text else "Pas de résumé disponible."

            pub_date_node = item.find('pubDate')
            pub_date = pub_date_node.text[:16] if pub_date_node is not None else "N/A"

            # Ajout de la colonne Résumé dans la ligne du tableau
            articles.append(f"| {pub_date} | [{title}]({link}) | {summary} | {source['nom']} | À analyser |")
    except Exception as e:
        print(f"Erreur sur {source['nom']}: {e}")

# Génération du tableau avec la colonne Résumé
table_content = f"""# 🛡️ Veille Automatique NIS 2 & Cybersécurité (BTS SIO)

*Mise à jour quotidienne automatique multi-sources via Python et GitHub Actions.*

| Date | Article / Titre | Résumé | Source Officielle | Statut |
| :--- | :--- | :--- | :--- | :--- |
""" + "\n".join(articles)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(table_content)

print("Tableau de veille avec résumés généré avec succès !")
