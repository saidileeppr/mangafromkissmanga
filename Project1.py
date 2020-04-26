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
Favlist=[]
Error_ch=[]
Error_page=[]
def update_file():
    f1=open('/home/saidileep/Documents/Python_Files/Favourites1.txt','w')
    for i in range(0,len(Favlist),2):
        f1.write(Favlist[i]+':'+str(Favlist[i+1])+'\n')
    f1.close()
def update_list(ns,ch):
    global Favlist,Error_ch,Error_page
    flag=0
    if(Favlist):
        for i in range(0,len(Favlist),2):
            if(ns==Favlist[i]):
                flag=1
                if(Favlist[i+1]<=ch):
                    Favlist[i+1]=ch
        if(flag==0):
            Favlist.append(ns)
            Favlist.append(ch)
    else:
        Favlist.append(ns)
        Favlist.append(ch)
    print('Current Uptodate',Favlist)
    update_file()
    print('Error Chapters:',Error_ch)
    print('Error pages:',Error_page)
def wimg(path1,ch,pg,i,ns):
    global Error_page
    try:
        os.system('wget -O '+path1+str(ch)+'-'+str(pg)+'.jpg'+'  '+i)
    except:
        Error_page.append(ns+str(ch)+':'+str(pg))
def downimg(i,name,ch,ns,pg):
    path=os.getcwd()
    path1=path+'/'+ns+'/'
    print('Downloading Ch'+str(ch)+' Page:'+str(pg))
    try:
        urllib.request.urlretrieve(i,path1+str(ch)+'-'+str(pg)+'.jpg')
    except :
        print("Error at "+str(ch)+' - '+str(pg))
        threading.Thread(target=wimg,args=(path1,ch,pg,i,ns)).start()
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
    update_list(ns,ch)
    f.close()
def getimg(ch,ln,ns,wd):
    global Error_ch
    image_list=[]
    wd.get(ln)
    page=wd.page_source
    soup=BeautifulSoup(page,'lxml')
    for i in soup.findAll('img'):
        s=i.get('src')
        if(not s.endswith('png')):
            if(not s.endswith('svg')):
                    image_list.append(str(s))
        elif('kissmanga' not in s and 'Content'not in s):
            image_list.append(str(s))
    if(image_list):
        pass
    else:
        print('Error Occured for '+ns+' chapter '+str(ch))
        Error_ch.append(ns+':'+str(ch))
        return 0
    threading.Thread(target=downCh,args=(image_list,ch,ns,wd)).start()
def getCh(link,last_chapter,ns):
    chapterlist=[]
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    wd = webdriver.Chrome(executable_path='/bin/chromedriver',chrome_options=chrome_options)
    wd.get(link)
    wait = WebDriverWait(wd, 10)
    h3 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#head > h1 > a")))
    ls='https://kissmanga.com'
    page=wd.page_source
    try:
        pass
    except:
        print("Error at:"+link)
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
        if(l and ls+s not in chapterlist):
            chapterlist.insert(0,ls+s)
    length=len(chapterlist)
    for i in range(0,length):
        print(str(i)+' . '+chapterlist[i])
    a=str(re.findall('[hr]+-[0-9]+',chapterlist[-1]))
    upchapter=int(a[4:-2])
    print('Above are the avaliable links')
    if(last_chapter==upchapter):
        update_list(ns,upchapter)
    else:
        for i in range(last_chapter,upchapter):
            a=str(re.findall('[hr]+-[0-9]+',chapterlist[i]))
            getimg(int(a[4:-2]),chapterlist[i],ns,wd)
    wd.close()
def getManga(FavFile):
    f=open(FavFile,'r+')
    s=''
    for i in f.read():
        if(i=='\n'and s!=''):
            name,last_chapter=s.split(':')
            link='https://kissmanga.com/Manga/'+name
            getCh(link,int(last_chapter),name)
            s=''
        else:
            s=s+str(i)
    f.close()
FavFile='/home/saidileep/Documents/Python_Files/Favourites.txt'
getManga(FavFile)