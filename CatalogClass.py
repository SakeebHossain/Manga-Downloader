import requests
from bs4 import BeautifulSoup
from MangaClass import *
class Catalog:
    """
    A catalog of all the manga available.
    """
    def __init__(self):
        self.rawCatalog = None
        self.alphaCatalog = None
        self.genreCatalog = None
        self.setup()
    
    def setup(self):
        soup = self.get_html()
        self.createCatalogs(soup)
        
        
    def get_html(self):
        """
        None -> BeautifulSoup
        
        Gets the html version of the mangalist from mangareader.net, and
        returns the parsed version.
        """
        url = 'http://www.mangareader.net/alphabetical'
        
        # get html of of webpage, parse with bs4
        res = requests.get(url)
        res.raise_for_status()
        html_doc = res.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        return soup
    
    def createCatalogs(self, soup):
        """
        BeautifulSoup -> None
        
        Finds all the manga titles on the page and creates two dictionaries;
        -raw_catalog, maps title -> url of chapter list page
        -alpha_catalog, maps first letter of title -> title
        """
        raw_catalog = {}
        alpha_catalog = {}
        genre_catalog = {}
        # find all anchor tags containing manga titles
        mangas = soup.select('div div div div div ul li a')
        
        # create raw_catalog
        for manga in mangas:
            try:
                manga_name = manga.string
                link = manga['href']
                raw_catalog[manga_name] = link           
            except:
                print("Failed to find a manga. Title was: ", manga_name)
            
            # create alpha_catalog
            first_letter = manga_name[0].upper()
            try:
                alpha_catalog[first_letter].append(manga_name)
            except:
                alpha_catalog[first_letter] = [manga_name]
            
            # create genre_catalog

            #m = Manga(manga_name, 'http://mangareader.net' + link)
        
            #for gen in m.genres:
                #try:
                    #genre_catalog[gen].append(manga_name) 
                #except:
                    #genre_catalog[gen] = [manga_name]
            #print(manga_name + ' --> ' + str(m.genres))  

                
        
        self.write_rawdict_to_file(raw_catalog, 'rawCatalog.txt')
        self.write_other_dict_to_file(alpha_catalog, 'alphaCatalog.txt')
        self.write_other_dict_to_file(genre_catalog, 'genreCatalog.txt')        
        self.rawCatalog = raw_catalog
        self.alphaCatalog = alpha_catalog
<<<<<<< HEAD
        print("Finished creating Catalog.")
    
    def write_rawdict_to_file(self, dictionary, file_name):
        my_file = open(file_name, "w")
        for key in dictionary:
            my_file.write(str(key) + '!@#' + str(dictionary[key]) + '\n')
        my_file.close()
    
    def write_other_dict_to_file(self, dictionary, file_name):
        my_file = open(file_name, "w")
        for key in dictionary:
            str_list = ''
            for item in dictionary[key]:
                str_list += item + '$%^'                
            my_file.write(str(key) + '!@#' + str_list + '\n')
        my_file.close()    
        
        
        
    def search(self, query):
            results = []
            for key in self.alphaCatalog.keys():
                for manga_name in self.alphaCatalog[key]:
                    if str(query) in manga_name:
                        results.append(manga_name)
            results.sort()
            return results    

##opening other_dict
#c = Catalog()
#raw = {}
#file = open('genreCatalog.txt', 'r')
#for next_line in file:
    #line = next_line.split('!@#')
    #line[1] = line[1].split('$%^')
    #raw[line[0]] = line[1][:-2]

#print(raw)
