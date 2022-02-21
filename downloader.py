from lib2to3.pgen2 import driver
from bs4 import BeautifulSoup as bs
from selenium import webdriver

import requests
import shutil
import os

from config import Setting

class Downloader:
    #hosts contain hosts of site where can load image from
    hosts = ["https://m.ac.qq.com/chapter/index/id/647289/cid/27"] #TODO: load data from json file in the next wersion
    hosts_ = ["https://m.ac.qq.com/", "https://tkr078.com/", "https://www.kuaikanmanhua.com/"] # Не менять порядок хостов
    
    made_files = []

    url = ""

    temp_path = ""
    path = ""
    character = ""

    def __init__(self, url = "", path = "D:\\", character = "1"):
        self.path = path
        self.temp_path = os.path.join(path, "temp\\")
        self.character = character
        self.url = url

    def get_lists_of_hosts(self):
        return self.hosts_


    def get_source_code_in_bs4(self, url):
        """ This function return will return 
            html code in beutifulSoup

            url: link to manga
        """
        print("[-] Getting session .... ")
        driver = webdriver.Firefox()
        print("[+] Session was got")


        print("[-] Get page ....")
        driver.get(url)   
        print("[+] Page is gotten")
        
        content = driver.page_source

        print("[-] Closing browser ....")
        driver.close()
        print("[+] Browser is closed")

        return bs(content, 'html.parser')

    
    def get_links_imgs_0(self, sorce_html ):
        """ Функция работает только с первм хостом https://m.ac.qq.com/
            
        """
        
        imgs = sorce_html.select(".comic-pic-list-all > ul > li > .comic-pic-box > .comic-pic")
        imgs_src = [img['data-src'] for img in imgs]
        return imgs_src


    def get_links_imgs_1(self, sorce_html):
        """ Функция работает только с первм хостом https://tkr078.com/
            
        """
        # print(sorce_html.find_all("img"))
        imgs = sorce_html.select(".contents > #tnimg > .img-tag")
        imgs_src = [img['src'] for img in imgs]
        return imgs_src
        # return 

    def get_links_imgs_2(self, sorce_html):
        imgs = sorce_html.select(".imgList > .img-box > .img")

        imgs_src = []  # i use this way coze in one section of pictures have two the same tag of html   
        for img in imgs:        #it's mean  <div class="img-box"> <img src="the_same"> <img src="the_same"> </div>
            if img.has_attr("data-src"):
                imgs_src.append(img['data-src'])
        
        return imgs_src

    def get_links_imgs(self, host_id, html):
        if(host_id == '0'):
            return self.get_links_imgs_0(html)
        elif (host_id == '1'):
            return self.get_links_imgs_1(html)
        elif (host_id == '2'):
            return self.get_links_imgs_2(html)

    def download(self, host_id, url, path="C:\\", charcter="0"):
        """host_id: id of the host 
            url: link to character of mangi
            path: where will be saved img
        """
        path_to_c = os.path.join(path, f"{charcter}\\")
        if (not os.path.exists(path_to_c)):
            os.makedirs(path_to_c)
        
        path_to_c = os.path.join(path_to_c, "temp\\")
        if (not os.path.exists(path_to_c)):
            os.makedirs(path_to_c)

        html = self.get_source_code_in_bs4(url)
        print("[-]Downloading imgs ....")

        try:
            imgs_src = self.get_links_imgs(host_id, html)
        except Exception as e:
            print(e)
            shutil.rmtree(path_to_c)
            return -1
            
        try:
            for i in range(len(imgs_src)):
                img_loc = os.path.join(path_to_c, f"{i+1}.jpg")
                r = requests.get(imgs_src[i], allow_redirects=True)
                open(img_loc, "wb").write(r.content)
        except Exception as e:
            print(e)
            shutil.rmtree(path_to_c)
            return -1
        print("[+] Imgs are downloaded")

        return 0

class Downloader_:
    hosts = ["https://m.ac.qq.com", "https://tkr078.com", "https://www.kuaikanmanhua.com"] # Не менять порядок хостов
    
    path_to_download_temp = ""
    url = ""
    host_id = ""

    def __init__(self, host_id=None, url=None, path="C:\\"):
        self.path_to_download_temp = os.path.join(path, Setting.temp_folder_name)
        self.url = url
        self.host_id = host_id

    def get_lists_of_hosts(self):
        return self.hosts

    def __get_source_code_in_bs4(self, url):
        """ This function return will return 
            html code in beutifulSoup

            url: link to manga
        """
        print("[-] Getting session .... ")
        driver = webdriver.Firefox()
        print("[+] Session was got")


        print("[-] Get page ....")
        driver.get(url)   
        print("[+] Page is gotten")
        
        content = driver.page_source

        print("[-] Closing browser ....")
        driver.close()
        print("[+] Browser is closed")

        return bs(content, 'html.parser')

    def __get_links_imgs_0(self, sorce_html ):
        """ Функция работает только с первм хостом https://m.ac.qq.com/
            
        """
        
        imgs = sorce_html.select(".comic-pic-list-all > ul > li > .comic-pic-box > .comic-pic")
        imgs_src = [img['data-src'] for img in imgs]
        return imgs_src


    def __get_links_imgs_1(self, sorce_html):
        """ Функция работает только с первм хостом https://tkr078.com/
            
        """
        # print(sorce_html.find_all("img"))
        imgs = sorce_html.select(".contents > #tnimg > .img-tag")
        imgs_src = [img['src'] for img in imgs]
        return imgs_src
        # return 

    def __get_links_imgs_2(self, sorce_html):
        print("[-] Getting links of the imgs ....")
        imgs = sorce_html.select(".imgList > .img-box > .img")

        imgs_src = []  # i use this way coze in one section of pictures have two the same tag of html   
        for img in imgs:        #it's mean  <div class="img-box"> <img src="the_same"> <img src="the_same"> </div>
            if img.has_attr("data-src"):
                imgs_src.append(img['data-src'])
        
        print("[+] Links are gotten")
        return imgs_src    


    def __get_links_imgs(self, host_id, sorce_code):
        if(host_id == '0'):
            return self.__get_links_imgs_0(sorce_code)
        elif (host_id == '1'):
            return self.__get_links_imgs_1(sorce_code)
        elif (host_id == '2'):
            return self.__get_links_imgs_2(sorce_code)

        return -1

    def __download_img(self, imgs_src):
        print("[-]Downloading imgs ....")
       
        for i in range(len(imgs_src)):
            img_loc = os.path.join(self.path_to_download_temp, f"{i+1}.jpg")
            r = requests.get(imgs_src[i], allow_redirects=True)
            open(img_loc, "wb").write(r.content)
        
        print("[+] Imgs are downloaded")
        

    def run_download(self):
        os.mkdir(self.path_to_download_temp)
        
        html = None
        try:    
            html = self.__get_source_code_in_bs4(self.url)
        except Exception as e:
            print(e)
            shutil.rmtree(self.path_to_download_temp)
            return -1


        imgs_src = None
        try:
            imgs_src = self.__get_links_imgs(self.host_id, html) 
        except Exception as e:
            print(e)
            shutil.rmtree(self.path_to_download_temp)
            return -1


        try:
            self.__download_img(imgs_src)
        except Exception as e:
            print(e)
            shutil.rmtree(self.path_to_download_temp)
            return -1

        return 0
    

        
        
        

if __name__ == "__main__":
    

    # dw = Downloader_("1", "https://tkr083.com/webtoon/416714/5627", "D:\\manglib\\test\\1")
    # dw.run_download()

    driver = webdriver.Chrome()
    
    driver.get("https://tkr083.com/webtoon/416714/5627")

    driver.close()