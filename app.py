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

    if (path is "" or url == ""):
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
    
def main():
    
    sites = Downloader_.get_lists_of_hosts(Downloader_)
    text_site = "\n"
    for site in sites:
        text_site += site +'\n'

    window = tk.Tk()
    window.title("Downloading imgs")
    window.geometry("1000x700")

    label1 = tk.Label(window, width=50, text="Downloading", anchor='w')
    label1.config(font=("Raleway", 16), justify=tk.CENTER)
    label1.pack(side=tk.TOP, pady=20, )


    lable_frame = tk.LabelFrame(window, text="Available sites")
    label2 = tk.Label(lable_frame, width=50, text=text_site , anchor='w')
    label2.config(font=("Raleway", 16))
    label2.pack()
    lable_frame.pack(side=tk.RIGHT, pady=20)

    label3 = tk.Label(window, width=50, text="url", anchor='w')
    label3.config(font=("Raleway", 16))
    label3.pack(side=tk.RIGHT, pady=20)

    entry1 = tk.Entry(window, width=50)
    entry1.pack(side=tk.TOP, pady=20)

    label4 = tk.Label(window, width=50, text="path", anchor='w')
    label4.config(font=("Raleway", 16))
    label4.pack(side=tk.TOP, pady=20)

    entry2 = tk.Entry(window, width=50)
    entry2.pack(side=tk.TOP, pady=20)

    b1 = tk.Button(window, text="CLICK ME!!!!!!", width=50, command=lambda : get_res(entry1, entry2))
    b1.config(font=("Raleway", 16), justify=tk.CENTER)
    b1.pack(side=tk.TOP, pady=20)


    window.mainloop()



if __name__ == "__main__":
    main()
    # lf = "https://docs.python.org/3/library/re.html"
    # split = re.split("/", lf)
    # print(split)
    # print(split[2])
    # print(re.search("//.+[.].+[.].+/",lf).group(0))