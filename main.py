from bs4 import BeautifulSoup
import requests
import os
import re
import json
import time
import random as ra
import multiprocessing as mp
import math as ma
from collections import Counter

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
        self.results = []
        self.times = 0
        self.count = 0
        self.fullNumOfWords = 0
        self.numOfWords = 0

    def tree_maker(self, url):
        page = requests.get(url)
        data = page.text
        soup = BeautifulSoup(data, features="html.parser")
        table = soup.find('ul', 'css-1lc0dpe et6tpn80')
        related_text = [x.text for x in table.find_all('a')]
        while True:
            for i in range(5):
                # print(related_text[i])
                self.word_tree.append(related_text[i])
            self.count += 1
            if self.count <= 3:
                self.tree_maker(self.init_url + related_text[i])
            else:
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

    def time_getter(self):
        # GET HOW MUCH TIME THEY HAVE THEN BASE THE AMOUNT OF WORDS OFF OF THAT
        pass

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
        self.fullNumOfWords = 1000
        new_names = [ra.choice(needed_names) for x in range(self.fullNumOfWords)]
        self.names_to_check = list(set(new_names))

    def initatior(self):
        print("init")
        now = time.time()
        with mp.Manager() as manager:
            fr = manager.list()
            num = manager.list()
            split_by = ma.floor(len(self.names_to_check) / 10)
            name1 = self.names_to_check[:split_by]
            name2 = self.names_to_check[split_by+1:(2*split_by)]
            name3 = self.names_to_check[(2*split_by)+1:(3*split_by)]
            name4 = self.names_to_check[(3*split_by)+1:(4*split_by)]
            name5 = self.names_to_check[(4*split_by)+1:(5*split_by)]
            name6 = self.names_to_check[(5*split_by)+1:(6*split_by)]
            name7 = self.names_to_check[(6*split_by)+1:(7*split_by)]
            name8 = self.names_to_check[(7*split_by)+1:(8*split_by)]
            name9 = self.names_to_check[(8*split_by)+1:(9*split_by)]
            name10 = self.names_to_check[(9*split_by)+1:]
            p1 = mp.Process(target=self.name_searcher, args=(name1, fr, num,))
            p2 = mp.Process(target=self.name_searcher, args=(name2, fr, num,))
            p3 = mp.Process(target=self.name_searcher, args=(name3, fr, num,))
            p4 = mp.Process(target=self.name_searcher, args=(name4, fr, num,))
            p5 = mp.Process(target=self.name_searcher, args=(name5, fr, num,))
            p6 = mp.Process(target=self.name_searcher, args=(name6, fr, num,))
            p7 = mp.Process(target=self.name_searcher, args=(name7, fr, num,))
            p8 = mp.Process(target=self.name_searcher, args=(name8, fr, num,))
            p9 = mp.Process(target=self.name_searcher, args=(name9, fr, num,))
            p10 = mp.Process(target=self.name_searcher, args=(name10, fr, num,))
            p1.start()
            p2.start()
            p3.start()
            p4.start()
            p5.start()
            p6.start()
            p7.start()
            p8.start()
            p9.start()
            p10.start()
            p1.join()
            p2.join()
            p3.join()
            p4.join()
            p5.join()
            p6.join()
            p7.join()
            p8.join()
            p9.join()
            p10.join()
            self.write(fr)
        print('\r', 'Done!', end='\n')
        print("time taken = " + str(time.time() - now))

    def name_searcher(self, list_name, final_results, num):
        for name in list_name:
            num.append(0)
            ETA = ((self.fullNumOfWords - len(num)) * 3)/15
            print('\r', str(len(num)), "words out of", str(self.fullNumOfWords), "done.", "\rEstimated Time left=", str(ETA), "seconds", end=' ')
            url1 = self.name_url1 + name
            page1 = requests.get(url1)
            data1 = page1.text
            soup1 = BeautifulSoup(data1, features="html.parser")
            count = 0
            for i in soup1.findAll('div', {'class':'rc5'}):
                word_list = i.text.strip().split()
                # if word_list[0] in acceptable:
                for word in self.word_tree:
                    if word in word_list:
                        count += 1
            for i in range(count):
                final_results.append(name)


    def write(self, res):
        result = Counter(res)
        print(result)
        with open("test.json", "w+") as file:
            dump = json.dumps(result, indent=4)
            file.write(dump)


if __name__ == '__main__':
    test = Request("Confident", "M", 1980, 1990)
    test.tree_maker(test.url)
    test.file_getter()
    test.name_getter()
    test.initatior()

