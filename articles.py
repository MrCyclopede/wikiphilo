import requests
import urllib
from bs4 import BeautifulSoup


def get_url_list():
    url = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Liste_d%27articles_que_toutes_les_encyclop%C3%A9dies_devraient_avoir"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features="html.parser")
    list_items = []
    links = []
    url_list = []

    div = soup.find("div", {"class": "mw-parser-output"})
    ordered_lists = div.find_all("ol")
    for list in ordered_lists:
        list_items += list.find_all("li")
    for item in list_items:
        links += item.find_all("a")

    for link in links:
        url_list.append(f"https://fr.wikipedia.org{link['href']}")

    return url_list

if __name__ == "__main__":
    print(get_url_list())