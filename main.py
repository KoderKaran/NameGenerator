from bs4 import BeautifulSoup
import requests
name_path = "C:\\Users\\yugio\\PycharmProjects\\NameGenerator\\names"

# USE THESE SITES TO CHECK:
# https://www.behindthename.com/name/john
# https://www.names.org/ THIS ONE IS BETTER


class Request:
    def __init__(self, trait, start_yr, end_yr):
        self.trait = trait  # MAKE A TREE OF SYNONYMS FOR TRAIT AND CHECK EACH NAME AGAINST THIS.
        self.start_year = start_yr
        self.end_year = end_yr
