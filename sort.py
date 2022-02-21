# #TODO: Авто удаление и добавление всех нужных путе temp, copy
from config import Setting

from PIL import Image

import shutil
import PIL
import os
import re


class Sort_:
    __dirs_with_pict = [] # array of tupple (folder, width, height)
    __path_to_manga = ""
    __path_to_manga_temp = ""
    __max_size = 20000
    __files_to_delete = [] #this file will be deleted after some critical Exceptione
    

    def __init__(self, path_to_mang="C:\\"):
        self.__path_to_manga = path_to_mang
        self.__path_to_manga_temp = os.path.join(path_to_mang, Setting.temp_folder_name)


    def __get_int_from_img(self, path):
        # it's need for sort imgs by ther count 
        m = re.search("\d+.jpg", path)
        file_name = m.group(0)
        num = int(re.search("\d+", file_name).group(0))
        return num
    
    def __getting_imgs_name(self, temp_dir):
    
        imgs = []
        print("[-] Getting files's names ....")
        for filename in os.listdir(temp_dir):
            imgs.append (temp_dir+ filename)
        print("[+] Files is gotten")
        return imgs
    

    def __sorting(self, imgs):
        count_character = 1
        curent_height = 0
        width = 0 
        

        curent_path_to_copy = os.path.join(self.__path_to_manga, f"{count_character}\\")         
        os.mkdir(curent_path_to_copy)
        self.__files_to_delete.append(curent_path_to_copy)

        print("[-] Sorting imgs .....")
        for img in imgs:
            #making pillow object
            img_pil = Image.open(img)
            width, height = img_pil.size
            
            #Overload  the availble place for img
            #Creating another one folder 
            if (curent_height + height > self.__max_size):
                self.__dirs_with_pict.append((curent_path_to_copy, width , curent_height))    
                
                count_character += 1
                curent_path_to_copy = os.path.join(self.__path_to_manga, f"{count_character}")
                os.makedirs(curent_path_to_copy)
                self.__files_to_delete.append(curent_path_to_copy)
                curent_height = 0
            
            curent_height += height
            img_pil.close()     
            shutil.copy(img, curent_path_to_copy)
        
        self.__dirs_with_pict.append((curent_path_to_copy, width , curent_height))#Последнее доьавление, чтобы занести в массив песледнюю созданный путь
        print("[+] Imgs are sorted")
       

    def __making_pict(self):
        print("[-] Making a picture ...")
        
        count = 1
        for dir, width_pic, height_pic in self.__dirs_with_pict:
            new_img = Image.new('RGB', (width_pic, height_pic))
            
            #getting paht to image
            files  = os.listdir(dir)
            files.sort(key=lambda x: self.__get_int_from_img(x))
            
            #make one image 
            height_pic_to_copy = 0
            for img in files:
                img = Image.open(os.path.join(dir, img))
                img_wid, img_heg = img.size
                
                #paste imge to one
                new_img.paste(img,(0, height_pic_to_copy))
                height_pic_to_copy += img_heg

            saves_path = os.path.join(self.__path_to_manga, Setting.folder_to_made_phot)

            if(not os.path.exists(saves_path)):
                os.makedirs(saves_path)
            self.__files_to_delete.append(saves_path)

            new_img.save(os.path.join(saves_path, f"{count}.jpg"))
            count+= 1   
        print("[+] Picture is made")


    def __remove_tmep_file(self):
        print("[-] Removeing temporary components....")
        shutil.rmtree(self.__path_to_manga_temp)
        for dir in self.__dirs_with_pict:
            shutil.rmtree(dir[0]) #dir[0] - it's path to folder
        print("[+] Components are removed")



    def run_sorting(self):

        # Массив с путями до картинок
        try:
            imgs = self.__getting_imgs_name(self.__path_to_manga_temp)
        except Exception as e:
            print(e)
            return -1 

        # Сортировка по числу из названии картинки 
        imgs.sort(key=lambda x: self.__get_int_from_img(x))

        try:
            self.__sorting(imgs)
        except Exception as e:
            print(e)
            for file in self.__files_to_delete:
                shutil.rmtree(file)
            return -1
        
        try:
            self.__making_pict()
        except Exception as e:
            print(e)
            for file in self.__files_to_delete:
                shutil.rmtree(file)
            return -1
        try:    
            self.__remove_tmep_file()
        except Exception as e:
            print(e)
            return -1

        return 0

if __name__ == "__main__":
    # a = Sort()
    # a.sorting("D:\manglib\обжора", '18')
    sr = Sort_("D:\\manglib\\test\\1")
    sr.run_sorting()
    