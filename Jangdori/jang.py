import subprocess
import requests
import codecs
import time
import sys
import os
import re
import io
from wand.image import Image
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlunparse
from urllib.request import urlretrieve, urlopen, Request

def get_jang() :
    url = 'http://news.khan.co.kr/kh_cartoon/khan_index.html?code=361102'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    for jang_div in soup.findAll('div', attrs={'class':'art_photo_wrap'}) :
        for jang_img in jang_div.findAll('img') :
            subject = str(jang_img).split('alt="')[1].split('"')[0]
            imgurl  = str(jang_img).split('src="')[1].split('"')[0]

            if subject == read_last_date() :
                pass #can't find new jangdori
            else :
                download_file(imgurl,'jang.jpg')
                send_telegram('http://ras.iptime.org/project/jang/jang.jpg', subject)
                write_last_date(subject)

def read_last_date() :
    f = codecs.open('./jang.txt', 'r', 'utf-8')
    return f.readlines()[0]

def write_last_date(subject) :
    f = codecs.open('./jang.txt', 'w', 'utf-8')
    f.write(subject)
    f.close()

def download_file(url,fnm) :
    try :
        if os.path.isfile(fnm) :
            os.remove(fnm)
        img = open(fnm,'wb')
        hrd = {'User-Agent':'Mozilla/5.0','referer':'http://www.khan.co.kr/'}
        req = Request(url, headers=hrd)
        res = urlopen(req)
        img.write(res.read())
        img.close()
    except :
        print('[ERROR]','[Download]',url)

def send_telegram(fileurl, subject) :
    TOKEN = '2995xxxxx:AAHpIs8ROUF6xxxxxxxxxxxxxxxxxxxxxxx'
    URL = 'https://api.telegram.org/bot%s/sendPhoto' % TOKEN
    CHAT_ID = '@today_jangdori'
    FILEURL = fileurl
    CAPTION = subject

    FILE = io.BytesIO(requests.get(FILEURL).content)
    FILE.name = FILEURL.split('/')[len(FILEURL.split('/'))-1]

    req = requests.post(URL, data = {'chat_id':CHAT_ID,'caption':CAPTION}, files = {'photo':FILE})
    #print(req.text)

get_jang()
