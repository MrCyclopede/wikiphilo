import requests
import re
from bs4 import BeautifulSoup


search = "internet truc"




def get_url_from_search(search_terms):
    search_formated = ""
    for x in search_terms.split():
        search_formated = search_formated + f"{x}+"

    search_url = f"https://fr.wikipedia.org/w/index.php?title=Sp%C3%A9cial:Recherche&go=Go&ns0=1&search={search_formated}"

    r = requests.get(search_url)
    soup = BeautifulSoup(r.content, features="html.parser")

    search_results_ul = soup.find("ul", {"class": "mw-search-results"})

    search_results_list_items = search_results_ul.find_all("li")

    first_result = search_results_list_items[0].find("a", href=True)
    first_result_url = first_result['href']

    wiki_url_prefix = "https://fr.wikipedia.org/"
    wiki_page_url = f"{wiki_url_prefix}{first_result_url}"
    return wiki_page_url


def get_article_content(page_url):
    r = requests.get(page_url)
    soup = BeautifulSoup(r.content, features="html.parser")

    content = soup.find("div", {"class": "mw-parser-output"})
    
    table_to_remove = soup.find_all("table")
    for d in table_to_remove:
        d.extract()
    
    div_to_remove = soup.find_all("div")
    for d in div_to_remove:
        d.extract()

    first_p = content.find_all("p")[0]
    return first_p
    

def find_first_link(article_content):
    print(article_content)

    # a = re.search("\)[^\(]*?<a.*?<\/a>", article_content)
    
    # print(a)
    # return a
    while(len(article_content)):
        
        link_begin = article_content.find("<a")
        link_end = article_content.find("/a>")

        print("\n\n\n=========")
        print(article_content)
        print(f"Testing:{article_content[link_begin:link_end]}")
        print(f"before char is: |{article_content[link_begin-1]}|")
        print(f"after char is: |{article_content[link_end + 3]}|")

        if article_content[link_begin - 1] not in [" ", ">"]:
            article_content = article_content[link_end + 3:]
            # print("invalid link, no space before") 

        elif article_content[link_end + 3] not in [" ", ",", ".", "?", "!", "<"]:
            article_content = article_content[link_end + 3:]
            # print("invalid link, no space or puncutation after") 

        else:
            # print(f"found link: '{article_content[link_begin - 1:link_end + 4]}'")
            return article_content[link_begin:link_end + 3]




        

    raise RuntimeError("no valid link found")

def get_first_link(page_url):
    article_content = str(get_article_content(page_url))
    link_content = find_first_link(article_content)


    suffix_start = link_content.find("/wiki")
    suffix_end = link_content[suffix_start:].find('"') + suffix_start

    link_suffix = link_content[suffix_start: suffix_end]
    

    wiki_url_prefix = "https://fr.wikipedia.org"

    return f"{wiki_url_prefix}{link_suffix}"
    
    
    




# def is_philosophie(url):
#     return url == "https://fr.wikipedia.org/wiki/Philosophie"
        
# url = "https://fr.wikipedia.org/wiki/Les_Cent_Trucs"
# while not is_philosophie(url):
#     print(url)
#     url = get_first_link(url)
# print("FOUND PHILOSOPHIE!!!!!!!!!!!!!!!!!")
# exit()
    
    


url_to_test = [
    # "https://fr.wikipedia.org/wiki/Les_Cent_Trucs",
    # "https://fr.wikipedia.org/wiki/Cin%C3%A9ma_muet",
    # "https://fr.wikipedia.org/wiki/Temps",
    "https://fr.wikipedia.org/wiki/Anglais",
    # "https://fr.wikipedia.org/wiki/R%C3%A9alit%C3%A9",
    # "https://fr.wikipedia.org/wiki/Alphabet_phon%C3%A9tique_international",
    # "https://fr.wikipedia.org/wiki/API_%C9%AA",
]


for url in url_to_test:
    print(get_first_link(url))



