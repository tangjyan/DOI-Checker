import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import winsound
import webbrowser
from win10toast import ToastNotifier


url1 = 'https://content.iospress.com/articles/international-journal-of-applied-electromagnetics-and-mechanics/jae209356'
url2 = 'https://doi.org/10.3233/JAE-209356'
url3 = 'https://content.iospress.com/journals/international-journal-of-applied-electromagnetics-and-mechanics/Pre-press/Pre-press'


def cheack(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    print(soup.title.text)
    return soup.title.text

def cheack1(url):
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'lxml')
    header = soup.select('h2>a')
    author = soup.select('a.badge')
    print(author[0].text) #+' / '+header[0].text.strip()
    return header[0].text


def timer(n):
    i=1
    while True:
        print('第'+str(i)+'次---'+datetime.now().strftime("%H:%M") +
              '---------')  # "%H:%M:%S"
        ch1=cheack(url1)
        
#        cheack(url2)
        chtitile=cheack1(url3)
        if i>1:
            if ch11!=ch1:
                winsound.Beep(600,2000)
                print(chtitile)
                webbrowser.open(url1)
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast("恭喜！！恭喜！！",
             "论文已见刊!")
        ch11=ch1        
        time.sleep(n)
        i=i+1


LastTime = input('扫描周期：')

timer(60*int(LastTime))
