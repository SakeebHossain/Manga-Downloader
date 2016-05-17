import os, requests
from bs4 import BeautifulSoup
import traceback
import CatalogClass


class Manga:
    """
    A class that store information about each manga title in the catalogs.
    """
    
    def __init__(self, title, url):
        """
        (String, String) -> None
        Instatiates manga object. 
        """
        self.title = title
        self.url = url
        self.release_date = "None!"
        self.ongoing = "None!"
        self.author = "None!"
        self.genres = "None!"
        self.manga_image = "None!"
        self.num_chapters = "None!"
        self.summary = "None!"
        self.setup(url)
    
    def setup(self, url):
        """
        (String) -> None
        Parses the manga homepage and fills in attributes defined in __init__
        """
        # Get the HTML of the main page for the manga (provided by the url)
        res = requests.get(url)
        res.raise_for_status()
        html_doc = res.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        # Select the table from the HTML that holds the manga info
        manga_info = soup.select('div div div div table tr td')
        
        self.release_date = manga_info[5].string  # Assign the release date
        
        # Assign True if ongoing, false otherwise
        if manga_info[7].string == 'Ongoing':
            self.ongoing = True
        else:
            self.ongoing = False       
        
        self.author = manga_info[9].string  # Assign name of author
        
        # Iterate through the provided genres (identified by having class
        #"genretags") and add them to a list 
        genres_list = []
        for genre in soup.find_all("span", class_="genretags"):
            genres_list.append(genre.string)
        self.genres = genres_list
        # might be able to simplify this to:
        # self.genres = soup.find_all("span", class_="genretags")

        self.manga_image = soup.find('img')['src']  # Grab URL of main image
        
        self.summary = soup.p.string  # Retrieve the manga summary
        
        list_chapters = soup.find(id="listing").find_all('a')
        self.num_chapters = list_chapters[-1].string.strip(self.title + ' ')
        
    def set_title(self, title):
        """
        (String) -> None
        Set the title of the manga.
        """
        self.title = title
    
    def set_url(self, url):
        """
        (String) -> None
        Set the URL of the manga.
        """        
        self.url = url
    
    def set_author(self, author):
        """
        (String) -> None
        Set the author of the manga.
        """        
        self.author = author
    
    def set_genres(self, genres):
        """
        (List of Strings) -> None
        Set the genres of the manga.
        """        
        self.genres = genres 
        
    def get_title(self):
        """
        (None) -> String
        Get the title of the manga.
        """
        return self.title
    
    def get_url(self):
        """
        (None) -> String
        Get the URL of the manga.
        """
        return self.url
    
    def get_author(self):
        """
        (None) -> String
        Get the author of the manga.
        """        
        return self.author
    
    def get_genres(self):
        """
        (None) -> List of String
        Get the genres of the manga.
        """        
        return self.genres
    
    def download_chapters(self, chapter_list):
        """
        List of int -> None
        """
        if not os.path.exists(self.title):
            os.makedirs(self.title)
        for chapter in chapter_list:
            os.makedirs(self.title + '/' + self.title + ' ' + str(chapter))
            chapter_url = self.url + '/' + str(chapter) + '/'
            page_counter = 1
            has_next_page = True
            try:
                while has_next_page:
                    page_url = chapter_url + str(page_counter)
                    print('Downloading ' + page_url + '...')
                    self.download_page(page_url, chapter, page_counter)
                    print("Downloading next page...")
                    page_counter += 1
            except:
                has_next_page = False
                print('Starting next chapter...')
        print('Finished!')

    
    def download_page(self, page_url, chapter, page_counter):
        img_url = self.get_img_url(page_url)
        res = requests.get(img_url)
        img_path = self.title + '/' + self.title + ' ' + str(chapter)
        img_title = self.title + ' ' + str(chapter) + '-' + str(page_counter) + '.jpg'
        imageFile = open(os.path.join(img_path, img_title), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    def get_img_url(self, page_url):
        print(page_url)
        res = requests.get(page_url)
        res.raise_for_status()
        html_doc = res.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        img_url = soup.find(id='img')['src']
        return img_url
