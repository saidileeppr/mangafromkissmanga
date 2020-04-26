from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import threading
def wimg(path1,ch,pg,i):
    os.system('wget -O '+path1+str(ch)+'-'+str(pg)+'.jpg'+'  '+i)
def downimg(i,name,ch,ns,pg):
    path=os.getcwd()
    path1=path+'/'+ns+'/'
    print('Downloading Ch'+str(ch)+' Page:'+str(pg))
    try:
        urllib.request.urlretrieve(i,path1+str(ch)+'-'+str(pg)+'.jpg')
    except :
        print("Error at "+str(ch)+' - '+str(pg))
        threading.Thread(target=wimg,args=(path1,ch,pg,i)).start()
    f=open(path1+name,'a+')
    f.write('\t\t<div>\n\t\t\t<center>\n')
    f.write('\t\t\t\t<img  src='+str(ch)+'-'+str(pg)+'.jpg'+' >\n')
    f.write('\t\t\t</center>\n\t\t</div>\n')
    f.close()
def downCh(image_list,ch,ns,wd):
    pg=1
    path=os.getcwd()
    path1=path+'/'+ns+'/'
    h1='''<!DOCTYPE html>
<html>
	<body bgcolor='#262626'>
'''
    name=str(ch)+'.html'
    os.system('mkdir '+ns)
    f=open(path1+name,'w+')
    f.write(h1)
    f.close()
    e1='''  </body>	
</html>'''
    for i in image_list:
        downimg(i,name,ch,ns,pg)
        pg=pg+1
    f=open(path1+name,'a+')
    f.write(e1)
    f.close()
def getimg(ch,ln,ns,wd):
    image_list=[]
    wd.get(ln)
    page=wd.page_source
    soup=BeautifulSoup(page,'lxml')
    for i in soup.findAll('img'):
        s=i.get('src')
        if(not s.endswith('png')):
            image_list.append(str(s))
    if(image_list):
        pass
    else:
        print('Error Occured for chapter '+str(ch))
        return 0
    threading.Thread(target=downCh,args=(image_list,ch,ns,wd)).start()
def getCh(link):
    chapterlist=[]
    ls='https://kissmanga.com'
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    wd = webdriver.Chrome(executable_path='/bin/chromedriver',chrome_options=chrome_options)
    wd.get(link)
    wait = WebDriverWait(wd, 10)
    h3 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#head > h1 > a")))
    page=wd.page_source
    soup=BeautifulSoup(page,'lxml')
    for i in soup.findAll('a'):
        s=i.get('href')
        l=re.findall('Chapter*',str(s))
        if(l and chapterlist==[]):
            chapterlist.insert(0,ls+s)
        if(l and ls+s != chapterlist[-1]):
            chapterlist.insert(0,ls+s)
        l=re.findall('Ch-x*',str(s))
        if(l and chapterlist==[]):
            chapterlist.insert(0,ls+s)
        if(l and ls+s!=chapterlist[-1]):
            chapterlist.insert(0,ls+s)
    f=link.split('/')
    ns=f[4]
    for i in range(0,len(chapterlist)):
        print(str(i)+' . '+chapterlist[i])
    print('Above are the avaliable links')
    mi=int(input('Enter starting chapter:'))
    ma=int(input('Enter ending chapter:'))
    for i in range(mi,ma+1):
        a=str(re.findall('-[0-9]+\?',chapterlist[i]))
        getimg(int(a[3:-3]),chapterlist[i],ns,wd)
    wd.close()
link='https://kissmanga.com/Manga/Magic-Emperor'
getCh(link)