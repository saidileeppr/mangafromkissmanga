from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import os
nt=0
def downimg(i,name,ch,ns,pg):
    path=os.getcwd()
    path1=path+'/'+ns+'/'
    os.system('wget -O '+path1+str(ch)+'-'+str(pg)+'.jpg'+'  '+i)
    f=open(path1+name,'a+')
    f.write('\t\t<div>\n\t\t\t<center>\n')
    f.write('\t\t\t\t<img  src='+str(ch)+'-'+str(pg)+'.jpg'+' >\n')
    f.write('\t\t\t</center>\n\t\t</div>\n')
def getimg(ch,ln,ns,wd):
    il=[]
    pg=1
    path=os.getcwd()
    path1=path+'/'+ns+'/'
    link=ln
    wd.get(link)
    time.sleep(1)
    wd.execute_script("window.stop();")
    page=wd.page_source
    soup=BeautifulSoup(page,'lxml')
    for i in soup.findAll('img'):
        s=i.get('src')
        l=re.findall('https://2.bp.blogspot.com*',str(s))
        if(l):
            il.append(str(s))
    if(il):
        pass
    else:
        print('Error Occured for chapter '+str(ch))
        return 0
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
    for i in il:
        downimg(i,name,ch,ns,pg)
        pg=pg+1
    f=open(path1+name,'a+')
    f.write(e1)
    f.close()
def Remove(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list 
def fun():
    il=[]
    link=str(input('Enter link:'))
    ls='https://kissmanga.com'
    wd=webdriver.Chrome(executable_path='/bin/chromedriver')
    wd.get(link)
    time.sleep(10)
    page=wd.page_source
    soup=BeautifulSoup(page,'lxml')
    for i in soup.findAll('a'):
        s=i.get('href')
        l=re.findall('Chapter*',str(s))
        if(l):
            il.append(ls+s)
        l=re.findall('Ch-x*',str(s))
        if(l):
            il.append(ls+s)
    il1=il[::-1]
    il=Remove(il1)
    f=link.split('/')
    ns=f[4]
    for i in range(0,len(il)):
        print(str(i)+' . '+il[i])
    print('Above are the avaliable links')
    mi=int(input('Enter starting chapter:'))
    ma=int(input('Enter ending chapter:'))
    for i in range(mi,ma+1):
        getimg(i,il[i],ns,wd)
    wd.close
fun()
