import os, requests
from bs4 import BeautifulSoup
import traceback
import Catalog


class Manga:
    
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.release_date = 'sniff'
        self.ongoing = 'sniff'
        self.author = 'sniff'
        self.genres = 'sniff'
        self.manga_image = 'sniff'
        self.num_chapters = 'sniff'
        self.summary = 'sniff'


        self.setup(url)
    
    def setup(self, url):
        """
        Parses the manga homepage and fills in the req'd info
        """
        res = requests.get(url)
        res.raise_for_status()
        html_doc = res.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        manga_info = soup.select('div div div div table tr td')
        
        self.release_date = manga_info[5].string
        
        if manga_info[7].string == 'Ongoing':
            self.ongoing = True
        else:
            self.ongoing = False       
        
        self.author = manga_info[9].string
        
        genres_list = []
        for genre in soup.find_all("span", class_="genretags"):
            genres_list.append(genre.string)
        self.genres = genres_list       

        self.manga_image = soup.find('img')['src'] 
        
        self.summary = soup.p.string
        
        list_chapters = soup.find(id="listing").find_all('a')
        self.num_chapters = list_chapters[-1].string.strip(self.title + ' ')
        
                
        
    def set_title(self, title):
        self.title = title
    
    def set_url(self, url):
        self.url = url
    
    def set_author(self, author):
        self.author = author
    
    def set_genres(self, genres):
        self.genres = genres 
        
    def get_title(self):
        return self.title
    
    def get_url(self):
        return self.url
    
    def get_author(self):
        return self.author
    
    def get_genres(self):
        return self.genres
    
    def download_chapters(self, chapter_list):
        """
        list of int -> None
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
