#coding = utf-8

import os
import time
import threading as td
import re
import codecs
import socket
import urllib.request
import requests
import bs4


def _getText(url, charset, targetPath, console):

    if console:
        print("Getting texts"+'-'*50)
        print("URL:", url)
        print("target path:", targetPath)

    #charset = soup.findAll(["meta", "script"], {"content":True})[0]["content"].split('=')[1]
    res = requests.get(url)
    res.encoding = charset
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    texts = soup.findAll(["a", "b", "c", "d", "e", "f", "i", "p",
                          "span", "li", "div", "pre"])

    def fTexts(texts): # filter texts
        filteredTexts = []
        for i in texts:
            if isinstance(i, bs4.element.Tag):
                filteredTexts.extend([j for j in i.contents])
            else:
                filteredTexts.append(i)
        return filteredTexts

    while any([isinstance(i,bs4.element.Tag) for i in texts]): # expand tags
        texts = fTexts(texts)
    else: # to prevent repeat and debug easily
        newTexts = []
        [newTexts.append(i) for i in texts if i not in newTexts]
        texts = newTexts

    with codecs.open(targetPath, 'w', charset) as file:
        for i in texts:
            file.writelines(i+"\n\n")

    if console: print("Done.\n")


def _getImg(url, targetDir, console, sleepTime):

    if console:
        print("Getting images"+'-'*50)
        print("URL:", url)
        print("Target directory:", targetDir)

    socket.setdefaulttimeout(30)
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
    AppleWebKit/537.36 (KHTML, like Gecko)')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    urllib.request.install_opener(opener)

    splitedURL = url.split("/")
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    picURLs = [tag["src"] for tag in soup.findAll("img", {"src":True})] # weak

    currentDir = os.sys.path[0]
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    os.chdir(targetDir)

    picNumbers = 0
    for picURL in picURLs:
        picName = os.path.basename(picURL[-251:])
        picName = picName if re.findall("\.jpg|\.png|\.gif", picName)\
                  else picName+".jpg"
        try: # some pic_url is fake or local
            if picURL[:3] == url[:3]: # absolute URL
                pass # remain picName same
            elif re.findall("//", picURL): # //something/something.something
                picURL = splitedURL[0] + picURL
            elif picURL[0] == "/": # /something/something.something
                picURL = "/".join(splitedURL[:3]) + picURL
            else: # something/something.something
                picURL = "/".join(splitedURL[:3]) + "/" + picURL
            urllib.request.urlretrieve(picURL, picName)
            time.sleep(sleepTime)
            picNumbers += 1
        except Exception as error:
            if console: print(error)

    os.chdir(currentDir)
    if console:
        print("Find %d pictures." %picNumbers)
        print("Done.\n")


def _getYoutubeVideo(url, fileName, targetPath, videoType, console):

    if console:
        print("Getting youtube video"+'-'*50)
        print("URL:", url)
        print("Target path:", targetPath+'/'+fileName+'.'+videoType)

    tube = pytube.YouTube(url)
    tube.set_filename(fileName)
    video = tube.get(videoType)

    for i in tube.get_videos():
        if console: print(i)
    if console: print("Downloading...")

    video.download(targetPath)
    if console: print("Done.\n")


def getText(url, charset="utf-8", targetPath="./text file.txt", console=True):
    thread = td.Thread()
    thread.run = lambda : _getText(url, charset, targetPath, console)
    thread.start()


def getImg(url, targetDir="./image folder", console=True, sleepTime=0):
    thread = td.Thread()
    thread.run = lambda : _getImg(url, targetDir, console, sleepTime)
    thread.start()


def getYoutubeVideo(url, fileName="youtube video", targetPath=".",
                    videoType="mp4", console=True): # "." means current path
    thread = td.Thread()
    thread.run = lambda : _getYoutubeVideo(url, fileName, targetPath,
                                           videoType, console)
    thread.start()


if __name__ == "__main__":

    url = "https://en.wikipedia.org/wiki/Oxygen"
    #getText(url, targetPath="./demo text file.txt")

    url = "https://en.wikipedia.org"
    getImg(url, targetDir="./demo images folder")

    url = "https://www.youtube.com/watch?v=BvA0J_2ZpIQ"
    #getYoutubeVideo(url, fileName="demo youtube video")
