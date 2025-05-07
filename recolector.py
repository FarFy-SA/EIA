import requests
from bs4 import BeautifulSoup

def recolectar_informacion(pregunta):
    query = pregunta.replace(" ", "+")
    url = f"https://lite.duckduckgo.com/lite/?q={query}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.find_all("a")

    textos = []
    for link in links[:3]:
        href = link.get("href")
        try:
            page = requests.get(href, timeout=5)
            inner_soup = BeautifulSoup(page.text, "html.parser")
            textos.append(inner_soup.get_text())
        except:
            continue

    return "\n".join(textos[:2])
