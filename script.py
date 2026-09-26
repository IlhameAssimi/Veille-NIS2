import urllib.request
import xml.etree.ElementTree as ET

# 1. URL du flux RSS du CERT-FR (ANSSI)
RSS_URL = "https://www.cert.ssi.gouv.fr/feed/"

try:
    # Récupération des données du flux RSS
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    xml_data = urllib.request.urlopen(req).read()
    root = ET.fromstring(xml_data)

    # Extraction des 5 derniers articles
    articles = []
    for item in root.findall('.//item')[:5]:
        title = item.find('title').text.replace('|', '-')
        link = item.find('link').text
        pub_date = item.find('pubDate').text[:16]
        articles.append(f"| {pub_date} | [{title}]({link}) | Automatique (CERT-FR) | À analyser |")

    # Mise à jour du fichier README.md
    table_content = """# 🛡️ Veille Automatique NIS 2 / Cybersécurité (BTS SIO)

*Cette veille est mise à jour automatiquement chaque jour via un script Python et GitHub Actions.*

| Date | Article / Source | Type | Statut |
| :--- | :--- | :--- | :--- |
""" + "\n".join(articles)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(table_content)

    print("Tableau de veille mis à jour !")

except Exception as e:
    print(f"Erreur lors de la mise à jour : {e}")
