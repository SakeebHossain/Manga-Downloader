import os, requests
from bs4 import BeautifulSoup
import CatalogClass


class Manga:
    """
    A class that store information about a specific manga title in the catalogs.
    We have one of each Manga class for each title in the raw catalogs
    
    Manga methods:
    - __init__()
    - setup()
    - getters/setters for : title, author, url, genre
    - download_chapters()
    - download_page()
    - get_img_url()
    
    To-do:
    - consider creating an layer of abstraction here. 
    - consider creating an update() function. 
    - maybe we want to have a 
    - something like a designated "manga library" where all manga will be 
      stored. This way we can update all the manga. 
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
        Given a url to a specific manga's info page, this function 
        parses it and fills in attributes defined in __init__
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
        try:
            self.num_chapters = list_chapters[-1].string.split(' ')[-1]        
        except:
            self.num_chapters = 'No chapters yet!'
        
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
        
        Given a list of numbers, downloads all the chapters of the manga whose
        chapter number is contained in the list.
        
        There are some shortcuts added in to make downloading easier.
        1. [1, 3, 60] : downloads chapters 1, 3 and 60.
        2. ['*'] : downloads all chapters.
        3. [1, '-', 6] : downloads chapters 1, 2, 3, 4, 5, and 6.
        
        The Chapters are downloaded into a folder with the structure:
        *Manga Title*/*Manga Title *Chapter Number*/*Manga Title* *Chapter Number*-*Page Number*
        i.e. Naruto/Naruto 1/Naruto 1-7
        
        To-do:
        - 
        
        """
     
        adjusted_title = self.title
        for punctuation in '!@#$%^&*+=~><\\/:;':
            adjusted_title = adjusted_title.replace(punctuation, '')
        
        ## ADDITION: Download all chapters
        if chapter_list == ['*']:
            chapter_list = range(1, int(self.num_chapters) + 1)
        #################################
        
        ## ADDITION: Download all chapters in a range
        # format example: [1, '-', 6] would download chapters 1,2,3,4,5 and 6
        # by replacing '-' with 2,3,4,5
        if "-" in chapter_list:
            dash_location = chapter_list.index("-")
            chapter_list.pop(dash_location)
            start_index = int(chapter_list.pop(dash_location-1))
            end_index = int(chapter_list.pop(dash_location-1)) + 1
            chapter_list.extend(range(start_index, end_index))
        #################################
        
        ## ADDITION: Make chapter list unique
        chapter_list = set(chapter_list)
        
        #################################         
            
        if not os.path.exists("Downloads/"+adjusted_title):
            os.makedirs("Downloads/"+adjusted_title)
        for chapter in chapter_list:
            os.makedirs("Downloads/"+adjusted_title + '/' + adjusted_title + ' ' + str(chapter))
            chapter_url = self.url + '/' + str(chapter) + '/'
            page_counter = 1
            has_next_page = True
            try:
                while has_next_page:
                    page_url = chapter_url + str(page_counter)
                    print('Downloading', self.title, "Chapter", chapter, "Page", page_counter)
                    self.download_page(page_url, chapter, page_counter)
                    page_counter += 1
            except:
                #traceback.print_exc()
                has_next_page = False
                print('Beginning download of next chapter')
        print('Finished!')

    
    def download_page(self, page_url, chapter, page_counter):
        adjusted_title = self.title
        for punctuation in '!@#$%^&*+=~><\\/:;':
            adjusted_title = adjusted_title.replace(punctuation, '')        
        img_url = self.get_img_url(page_url)
        res = requests.get(img_url)
        img_path = "Downloads/" + adjusted_title + '/' + adjusted_title + ' ' + str(chapter)
        img_title = adjusted_title + ' ' + str(chapter) + '-' + str(page_counter) + '.jpg'
        imageFile = open(os.path.join(img_path, img_title), 'wb')
        for chunk in res.iter_content(100000):
            imageFile.write(chunk)
        imageFile.close()

    def get_img_url(self, page_url):
        """
        (String) -> None
        
        Given a link to a specific page of a manga, returns the url of the img
        file on the page.
        """
        res = requests.get(page_url)
        res.raise_for_status()
        html_doc = res.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        img_url = soup.find(id='img')['src']
        return img_url