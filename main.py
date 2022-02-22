from downloader import Downloader_
from sort import Sort_
import os


def main():
    menu_ = """
0 - exit
1 - download img    
    """

    print(menu_)
    case = input()
    if case == '0':
        print("[-]Downloading ending")
        return 0
    if case != '1':
        print("[-]wrong input")
        return -1

    availabel_hosts = Downloader_.get_lists_of_hosts(Downloader_)

    print("[-]Available hostst: ")
    for i, host in enumerate(availabel_hosts):
        print(f"[{i}] {host}")

    print("\n\n[-]Chouse one: ")
    host_index = input()


    print("[-]enter url to manga")
    url = input()

    print("[-]Enter path to download(место со всеми главами)")
    path = input()


    dw = Downloader_(host_index, url, path) 
    dw.run_download()
   
    sr = Sort_(path)
    sr.run_sorting(path)



    return 0



if (__name__ == "__main__"):
    main()
    