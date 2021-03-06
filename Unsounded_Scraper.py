__author__ = 'Michael'
# Thanks to http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python

import urllib.request
import os
from multiprocessing.pool import Pool


def main():
    for i in range(1, 15):

        urls = []
        for j in range(1, 200):
            url = str("http://www.casualvillain.com/Unsounded/comic/ch" + str(i).zfill(2) + "/pageart/ch" + str(i).zfill(2) + "_" + str(j).zfill(2) + ".jpg")
            urls.append(url)

        # 2x as many processes as I have processors for better performance on more powerful systems, and because I may
        # get more speedup by utilising the time spent waiting for the website to respond.
        # Might not actually help though.
        with Pool(12) as p:
            p.map(download_file, urls)

        # Move downloaded files into a .cbr archive.
        rar_name = ("\"Chapter " + str(i) + ".cbr\"")
        os.system('rar m -m0 ' + rar_name + " *.jpg")


def download_file(url):
    filename = url.split("/")[-1]

    if not os.path.exists(filename): # Don't re-download files that are still sitting there from last time we ran
        try:
            urllib.request.urlretrieve(url, filename)
        except:
            pass

    if os.path.exists(filename):
        if os.path.getsize(filename) < 25 * 1024:
            os.remove(filename)


if __name__ == "__main__":
    main()
