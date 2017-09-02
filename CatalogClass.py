import requests
from multiprocessing import Queue
from bs4 import BeautifulSoup
from MangaClass import *

class Catalog:
    """
    A "catalog" of all the manga available. Each Catalog class has three
    "sub-catalogs". These sub-catalogues organize the manga titles in some 
    way. See the .createCatalogs() method for more details.
    
    Catalog methods:
    - __init__()
    - get_html()
    - createCatalogs()
    - search()
    """
    
    def __init__(self):
        self.rawCatalog = None
        self.alphaCatalog = None
        self.genreCatalog = None
        soup = self.get_html()  # retrieve bs4 of the manga list on the site
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
        - raw_catalog: a dict that maps 'title' -> 'url of chapter list page'
        - alpha_catalog: a dict that maps 'first letter of title' -> 'title'
        """
        raw_catalog = {}
        alpha_catalog = {}
        
        # find all anchor tags containing manga titles
        # i.e. <a href="www...com">One Piece</a>
        # .select returns an array of these anchor tags as strings
        mangas = soup.select('div div div div div ul li a')
        
        # Iterate through each manga/achor in mangas
        for manga in mangas:
            # Create the raw_catalog
            try:
                manga_name = manga.string  # .string gives what's b/w tags
                link = manga['href']  # retrieves the href link
                raw_catalog[manga_name] = link  # add the managa to raw
            except:
                print("Failed to find a manga. Title was: ", manga_name)
            
            # Create the alpha_catalog
            first_letter = manga_name[0].upper()  # get first letter of title
            try:
                # if a manga title starting with this letter already has
                # an entry, we can just append to its list
                alpha_catalog[first_letter].append(manga_name)  
            except:
                # if we haven't encountered a manga starting with that letter,
                # we just create the list!
                alpha_catalog[first_letter] = [manga_name]
                
       
        self.rawCatalog = raw_catalog
        self.alphaCatalog = alpha_catalog

        #print("Finished creating Catalog.")     
        
        
    def search(self, query):
            results = []
            for key in self.alphaCatalog.keys():
                for manga_name in self.alphaCatalog[key]:
                    if str(query) in manga_name:
                        results.append(manga_name)
            results.sort()
            return results    
