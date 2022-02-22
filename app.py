from fractions import Fraction
from sort import Sort_
from downloader import Downloader_
from tkinter import messagebox

import tkinter as tk
import re

def comand():
    pass

def get_host(url):
    """ url == https://www.google.com/  
    """
    return re.split('/', url)[2]

def path_is_right(path):
    return True    

def get_res(entry_url, entry_path):
    url = entry_url.get()
    path = entry_path.get()
    
    sites = Downloader_.get_lists_of_hosts(Downloader_)

    if(not path_is_right(path)):
        messagebox.showerror("showerror", "You entered the wrong path")
        return -1

    if (path == "" or url == ""):
        messagebox.showerror("showerror", "You did't fill a field")
        return -1

    host_id = None
    for i, site in enumerate(sites):
        host = get_host(url)  
        http_site = "http://" + host
        https_site = "https://" + host
        print(site, http_site, https_site)
        if (site == http_site or site == https_site):
            print(i)
            host_id = str(i)
            break
    
    if host_id is None:
        messagebox.showinfo("showinfo", "This site is not availble")
        return -1
    
    dn = Downloader_(host_id, url, path)
    status = dn.run_download()
    if (status == -1):
        messagebox.showerror("show_error", "The error has been happened during installation")
        return -1

    st = Sort_(path)
    status = st.run_sorting()

    if (status == -1):
        messagebox.showerror("show_error", "The error has been happened during sorting img")
        return -1


    messagebox.showinfo("show_info", "Installation success")
    return 0


def main_():
    window = tk.Tk()
    window.title("Downloading imgs")

    main_label = tk.Label(window, text="Downloading images", padx=20, pady=25)
    main_label.config(font=("Raleway", 32))
    main_label.grid(row=0, column=0, columnspan=2)

    
    list_of_availble_sites = Downloader_.get_lists_of_hosts(Downloader_)
    str_list_of_availble_sites = ""
    for site in list_of_availble_sites:
        str_list_of_availble_sites+= site + '\n'


    #CLUMN0 : row 0 The list of availbe sites is there
    frame_of_availble_sites_label = tk.LabelFrame(window, text="Availble sites:", font=("Raleway", 14))
    availble_sites_label = tk.Label(frame_of_availble_sites_label, text=str_list_of_availble_sites, padx=8, pady=5)
    availble_sites_label.config(font=("Raleway", 16))
    availble_sites_label.pack()
    frame_of_availble_sites_label.grid(row=1, column=0, rowspan=3)

    

    #COLUMN1 : row 1 - There is url placed
    row1 = tk.Frame(window)
    url_label = tk.Label(row1, text="url")
    url_label.config(font=("Raleway", 16))
    url_label.pack(side=tk.LEFT)
    url_entry = tk.Entry(row1)
    url_entry.pack(side=tk.RIGHT, padx=15)
    row1.grid(row=1, column=1)

    row2 = tk.Frame(window)
    path_label = tk.Label(row2, text="path")
    path_label.config(font=("Raleway", 16))
    path_label.pack(side=tk.LEFT)
    path_entry = tk.Entry(row2)
    path_entry.pack(side=tk.RIGHT, padx=15)
    row2.grid(row=2, column=1)

    buttom = tk.Button(window, text="CLICK ME!!!", command=lambda : get_res(url_entry, path_entry))
    buttom.grid(row=3, column=1)


    window.mainloop()

if __name__ == "__main__":
    main_()
    