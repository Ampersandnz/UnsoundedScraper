__author__ = 'Michael'
# Thanks to http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

import urllib.request
import os
from pathlib import Path
from multiprocessing.pool import Pool


def main():
    home = os.getcwd()
    for i in range(1, 2):
        download_dir = Path(os.getcwd() + "/Chapter " + str(i))

        if not download_dir.exists():
            download_dir.mkdir()
        os.chdir(download_dir.name)

        urls = []
        for j in range(1, 150):
            url = str("http://www.casualvillain.com/Unsounded/comic/ch" + str(i).zfill(2) + "/pageart/ch" + str(i).zfill(2) + "_" + str(j).zfill(2) + ".jpg")
            urls.append(url)

        # 2x as many processes as I have processors for better performance on more powerful systems, and because I may
        # get more speedup by utilising the time spent waiting for the website to respond.
        # Might not actually help though.
        with Pool(12) as p:
            p.map(download_file, urls)

        # Move downloaded files into a .cbr archive.
        rar_name = ("\"Chapter " + str(i) + ".cbr\"")
        os.system('rar m -m0 -msjpg ' + rar_name)

        os.chdir(home)


def download_file(url):
    filename = url.split("/")[-1]
    chapter = filename[2:4]

    try:
        urllib.request.urlretrieve(url, filename)
    except:
        pass

    if os.path.exists(filename):
        if os.path.getsize(filename) < 25 * 1024:
            os.remove(filename)
            print("Page " + filename + " of chapter " + chapter + " does not exist, temp file removed.")
        else:
            print("Page " + filename + " of chapter " + chapter + " retrieved!")


if __name__ == "__main__":
    main()