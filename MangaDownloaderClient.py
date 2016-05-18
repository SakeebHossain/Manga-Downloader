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
            try:
                print("Genres: " + manga.genres)
            except:
                print("Couldn't print genres!")
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
        """        
        #chapters.sort()
        if title in self.cat.rawCatalog.keys():
            try:
                url = 'http://www.mangareader.net' + self.cat.rawCatalog[title]
                manga = Manga(title, url)
                for i in chapters:
                    if i == '*' or i == '-':
                        pass
                    elif((type(i) != int) or (i > int(manga.num_chapters))):
                        print(str((i > int(manga.num_chapters))))
                        print(type(i) != int)
                        print('All items in chapter_list must be an int less '
                        'than ' + str(manga.num_chapters) + ' , which is the total '
                        'number of chapters available for ' + manga.title + '.')
                        return
                manga.download_chapters(chapters)
            except:
                print("Sorry, there was an error.")
                traceback.print_exc()
        else:
            print(title + " is an invalid title.")            

a = MangaDownloaderClient()


q = a.search('Bizarre')[2]
a.download_manga(q, [152])

#Yokohama Kaidashi Kikou

