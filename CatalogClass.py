import requests
from bs4 import BeautifulSoup

class Catalog:
    """
    A catalog of all the manga available for download.
    """
    
    def __init__(self):
        """
        (Catalog) -> None
        Sets up the dictionaries the two dictionaries we use to store info
        about each manga:
        -rawCatalog maps a the title of the manga to its homepage url
        -alphaCatalog maps each alphabet to a list of titles, all of which 
         start with that alphabet
        """
        self.rawCatalog = None  
        self.alphaCatalog = None
        soup = self.get_html()  # Retrieve the html of the page.
        self.createCatalogs(soup)  # Create the catalog.
    
    def get_html(self):
        """
        None -> bs4.BeautifulSoup
        
        Gets the html of the manga list from mangareader.net, and
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
        
        self.rawCatalog = raw_catalog
        self.alphaCatalog = alpha_catalog
        print("Finished creating Catalog.")
