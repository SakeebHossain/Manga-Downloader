from CatalogClass import *
from MangaClass import *
import traceback


class MangaDownloaderClient:
    
    def __init__(self):
        self.cat = Catalog()
    
    def search(self, query):
        try:
            results = self.cat.search(str(query))
            return results
        except:
            print("Invalid query!")
    
    def info(self, title):
        """
        Tells you info about the manga.
        """
        if title in self.cat.rawCatalog.keys():
            url = 'http://www.mangareader.net' + self.cat.rawCatalog[title]
            manga = Manga(title, url)        
            try:
                print("Title: " + manga.title)
            except:
                print("couldn't print title!")
            try:
                print("Release date: " + manga.release_date)
            except:
                print("couldn't print release date!")
            try:
                print("Author: " + manga.author)
            except:
                print("Couldn't print author!")
            #try:
                #print("Genres: " + manga.genres)
            #except:
                #print("Couldn't print genres!")
            try:
                print("No. Chapters: " + manga.num_chapters)
            except:
                print("Couldn't print release num chapters!")
            try:
                print("Summary: " + manga.summary)
            except:
                print("Couldn't print summary!")
        else:
            print("Invalid title!")
    
    def download_manga(self, title, chapters):
        """
        Method used to download the manga.
        
        Formatting:
        a = MangaDownloaderClient()
        
        a.download_manga(*proper manga title*, [*comma separated ints*]) #download specified chapters
        OR 
        a.download_manga(*proper manga title*, [*starting chapter*, '-', *ending chapter*]) #
        OR
        a.download_manga(*proper manga title*, ['*'])  #download ALL chapters
        """        
        #chapters.sort()
        if title in self.cat.rawCatalog.keys():
            try:
                url = 'http://www.mangareader.net' + self.cat.rawCatalog[title]
                manga = Manga(title, url)
                for i in chapters:
                    if i == '*' or i == '-':
                        pass
                    elif((int(i) > int(manga.num_chapters))):
                        print('Error: all items in chapter list must be an number less '
                        'than ' + str(manga.num_chapters) + ' , which is the total '
                        'number of chapters available for ' + manga.title + '.')
                        return
                manga.download_chapters(chapters)
            except:
                print("Sorry, there was an error.")
                #traceback.print_exc()
        else:
            print(title + " is an invalid title.")            