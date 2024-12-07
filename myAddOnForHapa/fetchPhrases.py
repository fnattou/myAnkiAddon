
import requests
import copy
import re
import pprint
from bs4 import BeautifulSoup
#https://beautiful-soup-4.readthedocs.io/en/latest/

class PhraseOfTheDay:
    def __init__(self):
        self.original_phrase = ""
        self.en = ""
        self.jp = ""
        self.example_eng = ""
        self.example_jp = ""
    
    def prettify(self):
        # self.example_jp = self.example_jp[1:-1]
        self.example_eng = self.example_eng[:-1]
        res = re.search("(\\d\\) )(.+)（(.*)）", self.original_phrase)
        if (res):
            self.en = res.group(2)
            self.jp = res.group(3)
        return
    
def scanSiblings(cur, n):
    res = cur
    for i in range(n):
        res = res.next_sibling
    return res

def fetch_phrases_of_the_day(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    todays_phrases_elem = soup.find("h4", string=re.compile("Phrases of the day"))
    if todays_phrases_elem is None:
        if __name__ == "__main__":
            print(url + " does not has phrases")
        return None

    phrase_list = []
    cur_phrase_title_elem = scanSiblings(todays_phrases_elem, 2)
    for i in range(5):
        phrase = PhraseOfTheDay()
        phrase.original_phrase = cur_phrase_title_elem.text
        example_element = scanSiblings(cur_phrase_title_elem, 4)
        if example_element.ul is None:
            example_element = scanSiblings(example_element, 2)
        if example_element.ul is None:
            example_element = scanSiblings(example_element, 2)
        phrase.example_eng = example_element.ul.li.b.text
        phrase.example_jp = example_element.ul.li.em.text
        phrase.prettify()
        phrase_list.append(phrase)
        cur_phrase_title_elem = scanSiblings(example_element, 2)

    return phrase_list

def fetch_podcast_url_list(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dl_list = soup.find_all("dl", id=re.compile("post-\\d*"))
    url_list = []
    title_list = []
    for dl in dl_list:
        url_list.append(dl.dt.h1.a.attrs['href'])
        title_list.append(dl.dt.h1.a.text)
    return [url_list, title_list]

def getTitleNum(title):
    m = re.search("\\d+", title)
    start = m.start()
    end = m.end()
    return title[start:end]

def isNormalTitle(title):
    m = re.match('第\\d+回「', title)
    return bool(m)

if __name__ == "__main__":
    rootUrl = 'https://hapaeikaiwa.com/blog/category/podcast-column'
    [url_list, title_list] = fetch_podcast_url_list(rootUrl)
    for i in range(0, len(url_list)):
        url = url_list[i]
        title = title_list[i]
        if getTitleNum(title) == "422":
            print("fetch from : " + title)
            phrase_list = fetch_phrases_of_the_day(url)
            for p in phrase_list:
                pprint.pprint(vars(p))