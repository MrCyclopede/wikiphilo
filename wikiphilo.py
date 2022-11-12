import requests
import urllib
from bs4 import BeautifulSoup
import articles

def get_first_result(search_results):

    soup = BeautifulSoup(search_results, features="html.parser")

    search_results_ul = soup.find("ul", {"class": "mw-search-results"})
    search_results_li = search_results_ul.find_all("li")

    first_result = search_results_li[0].find("a", href=True)
    first_result_url = first_result['href']

    return f"https://fr.wikipedia.org/{first_result_url}"


def resolve_page_for_search(search_terms):

    search_formated = " "
    for x in search_terms.split():
        search_formated = search_formated + f"{x}+"
    search_url = f"https://fr.wikipedia.org/w/index.php?title=Sp%C3%A9cial:Recherche&go=Go&ns0=1&search={search_formated}"
    
    r = requests.get(search_url)
    for code in r.history:
        if code.is_redirect:
            return r.url
    return get_first_result(r.content)


def remove_from_soup(soup):

    tags_to_remove = ["table", "div", "sup", "span"]
    for tag in tags_to_remove:
        to_remove = soup.find_all(tag)
        for item in to_remove:
            item.extract()
    
    p_to_remove = soup.find_all("p", {"class": "mw-empty-elt"})
    for p in p_to_remove:
        p.extract()


def get_article_links(page_url):
    r = requests.get(page_url)

    soup = BeautifulSoup(r.content, features="html.parser")
    divs = soup.find_all("div", {"class": "mw-parser-output"})

    for div in divs:
        if div.find("div", {"class": "nopopups"}):

            # TODO NOPOPUPS IS NOT A GOOD EXCLUSION : https://fr.wikipedia.org/wiki/Figueras
            continue
        # elif div.find("span", {"class": "noprint"}):
        #     continue
        else:
            remove_from_soup(div)
            tags = div.find_all(["p","li"])
            return tags
    

def find_first_link(tags):
    for tag in tags:
        a_list = tag.find_all("a")

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
    first_link = find_first_link(article_links)
    return f"https://fr.wikipedia.org{first_link}"


def is_philosophie(url):
    return url == "https://fr.wikipedia.org/wiki/Philosophie"


#=============== FROM ARTICLES LIST ==============

urls = articles.get_url_list()
for url in urls:
    print("\n\n=====================")
    jumps = 0
    while not is_philosophie(url):
        print(urllib.parse.unquote(url).split("/")[-1])
        try:
            url = get_first_link(url)
        except Exception as e:
            print("EXCEPTION: ", e)
            break
        jumps += 1
    print(f"Found Philosophie in {jumps} jumps")


#=============== FROM MANY SEARCH ==============

# search_term = ["internet truc", "minecraft", "Cinema muet", "Temps", "Anglais", "Realite", "alphabet phonetique international"]

# for term in search_term:
#     print(f'\n\nSearching for "{term}"\n')
#     url = resolve_page_for_search(term)

#     jumps = 0
#     while not is_philosophie(url):
#         print(urllib.parse.unquote(url).split("/")[-1])
#         url = get_first_link(url)
#         jumps += 1
#     print(f"Found Philosophie in {jumps} jumps")


# =============== FROM ONE==============

# url = "https://fr.wikipedia.org/wiki/Figueras"
# jumps = 0
# while not is_philosophie(url):
#     print(urllib.parse.unquote(url))
#     url = get_first_link(url)
#     jumps += 1
# print(f"Found Philosophie in {jumps} jumps")

    
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



