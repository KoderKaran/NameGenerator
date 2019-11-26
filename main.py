from bs4 import BeautifulSoup
import requests
import os
import re
import json
import random as ra
from collections import Counter
import time

# USE THESE SITES TO CHECK:
# https://www.behindthename.com/name/john
# https://www.names.org/ THIS ONE IS BETTER


class Request:
    def __init__(self, trait, gender, start_yr, end_yr, flag):
        self.flag = flag
        self.trait = trait.upper()
        self.gender = gender.upper()
        self.init_url = "https://www.thesaurus.com/browse/"
        self.url = "https://www.thesaurus.com/browse/" + trait
        self.name_url1 = "https://www.definitions.net/definition/"
        self.name_url2 = "https://www.behindthename.com/name/" # NAME
        self.start_year = start_yr
        self.end_year = end_yr
        self.word_tree = [self.trait]
        self.path = "C:\\Users\\yugio\\PycharmProjects\\NameGenerator\\names"
        self.open_files = []
        self.names_to_check = []
        self.results = []
        self.fullNumOfWords = 5000
        self.numOfWords = 0
        self.count = 0
        self.inp = 0

    def tree_maker(self, url):
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
        table = soup.find('ul', 'css-1lc0dpe et6tpn80')
        related_text = [x.text for x in table.find_all('a')]
        while True:
            for i in range(7):
                # print(related_text[i])
                self.word_tree.append(related_text[i].upper())
                self.word_tree.append(related_text[-1].upper())
            self.count += 1
            if self.count <= 4:
                self.tree_maker(self.init_url + related_text[i])
            else:
                break
        self.word_tree = list(set(self.word_tree))
        print(self.word_tree)

    def check(self):
        if self.flag:
            with open("results.json") as f:
                data = json.load(f)
            res = []
            for key in data.keys():
                if self.trait in data[key]:
                    res.append(key)
            for word in range(self.inp):
                if len(res) > 0:
                    element = ra.choice(res)
                    self.results.append(element)
                    res.remove(element)
        self.name_searcher()

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
        # make it loop through name amounts then plot it to see the times.
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
        num = self.num_getter()
        new_names = [ra.choice(needed_names) for x in range(self.fullNumOfWords)]
        self.names_to_check = list(set(new_names))
        self.check()

    def num_getter(self):
        inp = int(input("How many names do you want to get?"))
        self.inp = inp
        return inp

    def name_searcher(self):
        now = time.time()
        for name in self.names_to_check:
            if len(set(self.results)) >= self.inp:
                break
            print("\r", name, self.results, end='')
            url1 = self.name_url1 + name
            page1 = requests.get(url1)
            data1 = page1.text
            soup1 = BeautifulSoup(data1, features="html.parser")
            count = 0
            for i in soup1.findAll('div', {'class':'rc5'}):
                word_list = i.text.upper().strip().split()
                for word in self.word_tree:
                    if word in word_list:
                        count += 1
            for i in range(count):
                self.results.append(name)
        print("minutes taken: " + str((time.time() - now)/60))
        self.spit_results()

    def spit_results(self):
        result = Counter(self.results)
        print("These are the top names that match the word " + self.trait + ":")
        for r in result:
            print(r)
        self.write(result)

    def write(self, res):
        with open("results.json") as file:
            data = json.load(file)
        with open("results.json", "w") as f:
            for word in res.keys():
                if word not in data.keys():
                    data[word] = list()
                if self.trait not in data[word]:
                    data[word].append(self.trait)
            json.dump(data, f, indent=4)
        print("done")


if __name__ == '__main__':
    trait = input("What trait to search for?")
    gender = input("What gender to search for?(M/F)")
    startyr = int(input("Start year?"))
    endyr = int(input("End year?"))
    inp = input("Want results from database?Y/N")
    flag = True
    if inp == 'N':
        flag = False
    test = Request(trait, gender, startyr, endyr, flag)
    test.tree_maker(test.url)
    test.file_getter()
    test.name_getter()


