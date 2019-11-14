from bs4 import BeautifulSoup
import requests
import os
import re
import json
import time
import random as ra

# USE THESE SITES TO CHECK:
# https://www.behindthename.com/name/john
# https://www.names.org/ THIS ONE IS BETTER


class Request:
    def __init__(self, trait, gender, start_yr, end_yr):
        self.trait = trait
        self.gender = gender.upper()
        self.init_url = "https://www.thesaurus.com/browse/"
        self.url = "https://www.thesaurus.com/browse/" + trait
        self.name_url1 = "https://www.definitions.net/definition/"
        self.name_url2 = "https://www.behindthename.com/name/" # NAME
        self.start_year = start_yr
        self.end_year = end_yr
        self.word_tree = [trait]
        self.path = "C:\\Users\\yugio\\PycharmProjects\\NameGenerator\\names"
        self.open_files = []
        self.names_to_check = []
        self.count = 0
        self.results = {}
        self.times=0

    def tree_maker(self, url):
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
        table = soup.find('ul', 'css-1lc0dpe et6tpn80')
        related_text = [x.text for x in table.find_all('a')]
        while True:
            for i in range(5):
                print(related_text[i])
                self.word_tree.append(related_text[i])
            self.count += 1
            if self.count <= 3:
                self.tree_maker(self.init_url + related_text[i])
            else:
                print("done")
                break
        self.word_tree = list(set(self.word_tree))

    def file_getter(self):
        os.chdir(self.path)
        all_files = os.listdir(self.path)
        index1 = 0
        index2 = 0
        for file in all_files:
            if str(self.start_year) in file:
                index1 = all_files.index(file)
            if str(self.end_year) in file:
                index2 = all_files.index(file)
        needed_files = all_files[index1:index2+1]
        for new_file in needed_files:
            with open(new_file, 'r') as f:
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
        new_names = [ra.choice(needed_names) for x in range(1000)]
        self.names_to_check = list(set(new_names))

    def name_searcher(self):
        # second_link_catcher = re.compile("(?<=Meaning & History)(.*)(?=See All Relations)", re.MULTILINE | re.DOTALL)
        acceptable = ["Princeton's", "Wiktionary", "Freebase", "Webster Dictionary", "Chambers 20th", "The Nuttall"]
        print(len(self.names_to_check))
        start = time.time()
        for name in self.names_to_check:
            now = time.time()
            print(name)
            words_in_meaning = []
            url1 = self.name_url1 + name
            # url2 = self.name_url2 + name
            page1 = requests.get(url1)
            # page2 = requests.get(url2)
            data1 = page1.text
            # data2 = page2.text
            soup1 = BeautifulSoup(data1, features="html.parser")
            # soup2 = BeautifulSoup(data2, features="html.parser")
            full_text = ''
            for i in soup1.findAll('div', {'class':'rc5'}):
                for j in acceptable:
                    if j in i.text:
                        full_text+=i.text.strip()
            # for x in soup2.findAll('article'):
            #     all_matches = re.findall(second_link_catcher, x.text)
            #     for i in all_matches:
            #         full_text+=i.strip()
            text_list = full_text.split()
            for word in text_list:
                if word in self.word_tree:
                    words_in_meaning.append(word)
            if len(words_in_meaning) > 0:
                self.results[name] = len(words_in_meaning)
            print(time.time()-now)
            self.times+=time.time()-now
        print("avg time: " + str(self.times/ len(self.names_to_check)))
        print("total: " + str(time.time()-start))
        with open("test.json", "w+") as file:
            json.dump(self.results, file, indent=4)

            # get text from both soup1 and 2
            # whenever word from self.word_tree in text, append that word to words in meaning
            # store len of words_in_meaning
            # at the end, use Counter to get top word
            #
            # put the name as the key and tuple of: (top word, num of times top word, len of words_in_meaning) as
            # value in self.results


test = Request("Confident", "M", 1880, 1980)
test.tree_maker(test.url)
test.file_getter()
test.name_getter()
test.name_searcher()
