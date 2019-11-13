from bs4 import BeautifulSoup
import requests
import os
import re

# USE THESE SITES TO CHECK:
# https://www.behindthename.com/name/john
# https://www.names.org/ THIS ONE IS BETTER


class Request:
    def __init__(self, trait, gender, start_yr, end_yr):
        self.trait = trait  # MAKE A TREE OF SYNONYMS FOR TRAIT AND CHECK EACH NAME AGAINST THIS.
        self.gender = gender.upper()
        self.init_url = "https://www.thesaurus.com/browse/"
        self.url = "https://www.thesaurus.com/browse/" + trait
        self.start_year = start_yr
        self.end_year = end_yr
        self.word_tree = [trait]
        self.path = "C:\\Users\\yugio\\PycharmProjects\\NameGenerator\\names"
        self.open_files = []
        self.names_to_check = []
        self.count = 0

    def tree_maker(self, url):
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

    def word_getter(self):
        os.chdir(self.path)
        all_files = os.listdir(self.path)
        count = 0
        for file in all_files:
            with open(file, 'r') as f:
                self.open_files.append(f.read())

    def name_getter(self):
        name_catcher = re.compile("(\w+),([A-Z]),(\d+)")
        all_names = []
        for i in self.open_files:
            catch = re.findall(name_catcher, i)
            all_names += catch
        needed_names = []
        for g in all_names:
            gender = g[1]
            if gender == self.gender:
                needed_names.append(g[0])
        self.names_to_check = list(set(needed_names))


test = Request("ass", "f", 1000, 1500)
test.word_getter()
test.name_getter()
