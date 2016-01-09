from CatalogClass import *
from MangaClass import *

class MangaDownloaderClient:
    
    def __init__(self):
        self.cat = Catalog()
    
    def search(self, query):
        try:
            self.cat.search(str(query))
        except:
            print("Invalid query!")
    
    def download_manga(self, title, chapters):
        """
        
        """
        chapters.sort()
        if title in self.cat.rawCatalog.keys():
            try:
                url = 'http://www.mangareader.net' + self.cat.rawCatalog[title]
                manga = Manga(title, url)
                for i in chapters:
                    if((type(i) != 'int') or (i > manga.num_chapters)):
                        print('All item in chapter_list must be an int less '
                        'than ' + manga.num_chapters + ' , which is the total '
                        'number of chapters available for ' + manga.title + '.')
                        raise Exception()
                manga.download_chapters(chapters)
            except:
                print("Sorry, there was an error.")
        else:
            print(title + " is an invalid title.")            


    
    
    
