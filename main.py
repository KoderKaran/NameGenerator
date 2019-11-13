from bs4 import BeautifulSoup, SoupStrainer
import requests
name_path = "C:\\Users\\yugio\\PycharmProjects\\NameGenerator\\names"

# USE THESE SITES TO CHECK:
# https://www.behindthename.com/name/john
# https://www.names.org/ THIS ONE IS BETTER


class Request:
    def __init__(self, trait, start_yr, end_yr):
        self.trait = trait  # MAKE A TREE OF SYNONYMS FOR TRAIT AND CHECK EACH NAME AGAINST THIS.
        self.init_url = "https://www.thesaurus.com/browse/"
        self.url = "https://www.thesaurus.com/browse/" + trait
        self.start_year = start_yr
        self.end_year = end_yr
        self.word_tree = [trait]
        self.count = 0

    def treeMaker(self, url):
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data)
        table = soup.find('ul', 'css-1lc0dpe et6tpn80')
        related_text = [x.text for x in table.find_all('a')]
        while True:
            for i in range(5):
                print(related_text[i])
                self.word_tree.append(related_text[i])
            self.count += 1
            if self.count <= 10:
                self.treeMaker(self.init_url + related_text[i])
            else:
                print("done")
                break
        self.word_tree = list(set(self.word_tree))


test = Request("ass", 1000, 1500)
