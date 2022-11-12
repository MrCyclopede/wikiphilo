import requests
import re
from bs4 import BeautifulSoup


search = "internet truc"




def get_url_from_search(search_terms):
    search_formated = ""
    for x in search_terms.split():
        search_formated = search_formated + f"{x}+"

    search_url = f"https://fr.wikipedia.org/w/index.php?title=Sp%C3%A9cial:Recherche&go=Go&ns0=1&search={search_formated}"
    print(search_url)
    
    r = requests.get(search_url)
    print(r.history)
    soup = BeautifulSoup(r.content, features="html.parser")

    search_results_ul = soup.find("ul", {"class": "mw-search-results"})

    search_results_list_items = search_results_ul.find_all("li")

    first_result = search_results_list_items[0].find("a", href=True)
    first_result_url = first_result['href']

    wiki_url_prefix = "https://fr.wikipedia.org/"
    wiki_page_url = f"{wiki_url_prefix}{first_result_url}"
    return wiki_page_url


def remove_from_soup(soup):
    table_to_remove = soup.find_all("table")
    for d in table_to_remove:
        d.extract()
    
    div_to_remove = soup.find_all("div")
    for d in div_to_remove:
        d.extract()
    
    sup_to_remove = soup.find_all("sup")
    for d in sup_to_remove:
        d.extract()

    span_to_remove = soup.find_all("span")
    for d in span_to_remove:
        d.extract()
    
    p_to_remove = soup.find_all("p", {"class": "mw-empty-elt"})
    for d in p_to_remove:
        d.extract()


def get_article_links(page_url):
    r = requests.get(page_url)

    soup = BeautifulSoup(r.content, features="html.parser")

    divs = soup.find_all("div", {"class": "mw-parser-output"})

    for d in divs:
        if d.find("div", {"class": "nopopups"}):
            continue
        else:
            div = d
            break
    
    remove_from_soup(div)
    
    p_tags = div.find_all(["p","li"])

    return p_tags

def find_first_link(p_tags):
    for p_tag in p_tags:
        
        a_list = p_tag.find_all("a")

        for link in a_list:
            link = str(link)
            if "wiktionary.org" in link:
                continue
            link_begin = link.find('/wiki/')
            link_end = link[link_begin + 1:].find('"') + 1
            suffix = link[link_begin:link_end + link_begin]
            if not "API" in suffix:
                return suffix

    raise RuntimeError("no valid link found")

def get_first_link(page_url):
    article_links = get_article_links(page_url)
    
    flink = find_first_link(article_links)
    

    wiki_url_prefix = "https://fr.wikipedia.org"

    return f"{wiki_url_prefix}{flink}"
    
    
    




def is_philosophie(url):
    return url == "https://fr.wikipedia.org/wiki/Philosophie"
        

# =============== FROM ONE==============
url = "https://fr.wikipedia.org/wiki/Laitue"
jumps = 0
while not is_philosophie(url):
    print(url)
    url = get_first_link(url)
    jumps += 1
print(f"FOUND in {jumps} jumps")



#=============== FROM MANY SEARCH ==============
# search_term = ["internet truc", "minecraft"]

# for term in search_term:
#     url = get_url_from_search(term)

#     jumps = 0
#     while not is_philosophie(url):
#         print(url)
#         url = get_first_link(url)
#         jumps += 1
#     print("FOUND in {jumps} jumps")
    
    
#=============== TESTS ==============

# url_to_test = [
#     "https://fr.wikipedia.org/wiki/Les_Cent_Trucs",
#     "https://fr.wikipedia.org/wiki/Cin%C3%A9ma_muet",
#     "https://fr.wikipedia.org/wiki/Temps",
#     "https://fr.wikipedia.org/wiki/Anglais",
#     "https://fr.wikipedia.org/wiki/R%C3%A9alit%C3%A9",
#     "https://fr.wikipedia.org/wiki/Alphabet_phon%C3%A9tique_international",
#     "https://fr.wikipedia.org/wiki/Anthropologie",
#     "https://fr.wikipedia.org/wiki/Casquette",
    # "https://fr.wikipedia.org/wiki/Latin",
#         "https://fr.wikipedia.org/wiki/Polissage",
# ]


# for url in url_to_test:
#     print(get_first_link(url))



