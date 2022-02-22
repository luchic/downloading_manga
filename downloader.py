from cProfile import label
from lib2to3.pgen2 import driver
from bs4 import BeautifulSoup as bs
from click import pass_obj
from selenium import webdriver

import requests
import shutil
import os

from config import Setting


class Downloader_:
    hosts = ["https://m.ac.qq.com", "https://tkr078.com", "https://www.kuaikanmanhua.com", "https://m.kuaikanmanhua.com"] # Не менять порядок хостов
    
    

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
        elif (host_id == '3'):
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
    # db = Downloader_()
    # db.dict_keep_of_sites["https://m.ac.qq.com"]("<html></html>")
    pass