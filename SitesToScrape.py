path = "C:\\Users\\yugio\\PycharmProjects\\NameGenerator\\sites.txt"
sites = []


def addSite(new_site):
    with open(path, "a+") as file:
        file.write(new_site + '\n')


def getSites():
    with open(path) as file:
        lines = file.read().splitlines()
        for site in lines:
            sites.append(site)

# addSite("https://www.familyeducation.com/baby-names/renamer")
# addSite("https://bigthink.com/mind-brain/names-and-personality")
print(sites)
getSites()
print(sites)
