import requests
import shutil
import json
import os
import re
#user: botrob732368@gmail.com
#pass: -RhUUye25V(#$-6+


class image_getter():
    artistCode = ''
    urlList = []
    imagesDir = ""

    def __init__(self, rootfolder, artcode = ''):
        self.imagesDir = rootfolder
        self.artistCode = artcode

    def get_images(self, target = ''):
        # download image from url
        if not os.path.isdir(target):
            os.mkdir(target)
        headers = {"Host": "i.pximg.net",
                   "Referer": "https://www.pixiv.net",
                   "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
                   "Accept": "image/webp,*/*;q=0.8",
                   "Accept-Language": "en-US,en;q=0.5",
                   "Accept-Encoding": "gzip, deflate, br",
                   "DNT": "1",
                   "Connection": "keep-alive",
                   "Upgrade-Insecure-Requests": "1",
                   "If-Modified-Since": "Fri, 18 Sep 2020 12:20:51 GMT",
                   "Cache-Control": "max-age=0",
                   "TE": "Trailers"}
        for url in self.urlList:
            print(url)
            html = requests.get(url).text
            link = re.split("(http[s]*://i.pximg.net/img-original/.*?.(png|jpeg|jpg))", html)
            if len(link) > 2:
                link = link[1]
                resp = requests.get(link, headers=headers, stream=True)
                resp.raw.decode_content = True
                picture = link.split('/')
                targetpath = os.path.join(target, picture[-1])
                targetfile = open(targetpath, 'wb')
                shutil.copyfileobj(resp.raw, targetfile)
                targetfile.close()

    def get_urls(self, url):
        # get all urls from section of site
        resp = requests.get('https://www.pixiv.net/ajax/user/' + self.artistCode + '/profile/all?lang=en')
        json_text = resp.json()
        for id in json_text['body']['illusts']:
            self.urlList.append('https://www.pixiv.net/en/artworks/' + id)

    def crawl_site(self, codartist, target = ''):
        # get metadata from site and crawl downloading images
        self.artistCode = str(codartist)
        url = 'https://www.pixiv.net/en/users/' + self.artistCode + '/artworks'
        self.get_urls(url)
        self.get_images(target)

if __name__ == "__main__":
    totally_not_hentai = image_getter(os.path.dirname(os.path.realpath(__file__)))
    code = input("Input artist code: ")
    foldername = input("Input target folder: ")
    totally_not_hentai.crawl_site(code, foldername)