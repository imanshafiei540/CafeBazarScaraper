#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
import sqlite3
from flask import *
from flask_login import *
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import mechanize
import urllib
import re, urlparse






app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')


@app.route('/search&p=<page>',methods=['GET','POST'])
def showResult(page):

    def urlEncodeNonAscii(b):
        return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

    def iriToUri(iri):
        parts= urlparse.urlparse(iri)
        return urlparse.urlunparse(
            part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
            for parti, part in enumerate(parts)
        )


    if request.method == 'POST':
        name = request.form['name']
        name = iriToUri(name)
        #first test
        '''html=urllib.urlopen(url)
        soup = bs(html)
        for tag in soup.findAll('a',href=True):
            print tag['href']
            print "done"
            print tag'''

        #second test
        """url="https://cafebazaar.ir/"
        br=mechanize.Browser()
        br.open(url)
        for link in br.links():
            print link.base_url+link.url
        """
        def search(key,page):
            keys=key.rsplit()
            fkey=""
            for i in keys:
                fkey+=i
                if(i!=keys[-1]):
                    fkey+="+"
            result="https://cafebazaar.ir/search/?q="+fkey+"&l=fa&partial=true&p="+page
            return result
        url=search(name,page)
        #print url
        html=urllib.urlopen(url)
        soup=bs(html, 'lxml')
        bs()
        apps=soup.find_all('div',{"class":"msht-app"})
        #print type(apps)
        #print len(apps)
        apps=soup.findAll('div',{"class":"msht-app"})
        imgs=[i.find('img')['src'] for i in apps]

        #img= apps[0].find('img')
        #print img['src']
        names=[i.find('div',{"class":"msht-app-name"}).find('span') for i in apps]
        names=[i.contents[0] for i in names]
        #print names[0]
        #msht-app-price
        #print names[0].contents[0].encode('utf-8')
        tmp=[" ".join(i.rsplit()) for i in names]
        names=tmp
        #print names
        prices=[i.find('div',{"class":"msht-app-price"}).find('span') for i in apps]
        prices=[i.contents[0].rsplit()[0] for i in prices]
        #print prices
        links=["https://cafebazaar.ir"+i.find('a')['href'].rsplit()[0] for i in apps]

        new_links = []
        for link in links:

            position = link.find('app/')
            position2 = link.find('?')

            new_links.append(link[position+4:position2-1])






        #print links
        #print names[0].encode('utf-8')
        #names,prices,links,imgs =====>inast:D
        dic = {}
        #print len(imgs),len(prices),len(links),len(names)
        for i in range(len(imgs)):
            dic[imgs[i]] = (names[i], prices[i], new_links[i])
        #print dic
        return render_template('results.html',data_dic = dic, p=page , name=name)

@app.route('/search', methods=['GET', 'POST'])
def search():


    if request.method == 'POST':
        name = request.form['name']
        name = urlEncodeNonAscii(name)
        print name
        #first test
        '''html=urllib.urlopen(url)
        soup = bs(html)
        for tag in soup.findAll('a',href=True):
            print tag['href']
            print "done"
            print tag'''

        #second test
        """url="https://cafebazaar.ir/"
        br=mechanize.Browser()
        br.open(url)
        for link in br.links():
            print link.base_url+link.url
        """
        def search(key):
            keys=key.rsplit()
            fkey=""
            for i in keys:
                fkey+=i
                if(i!=keys[-1]):
                    fkey+="+"
            result="https://cafebazaar.ir/search/?q=" + fkey + "&l=fa&partial=true&p=0"

            return result
        url=search(name)


        html=urllib.urlopen(url)
        soup=bs(html, 'lxml')
        bs()
        apps=soup.find_all('div',{"class":"msht-app"})
        #print type(apps)
        #print len(apps)
        apps=soup.findAll('div',{"class":"msht-app"})
        imgs=[i.find('img')['src'] for i in apps]

        #img= apps[0].find('img')
        #print img['src']
        names=[i.find('div',{"class":"msht-app-name"}).find('span') for i in apps]
        names=[i.contents[0] for i in names]
        #print names[0]
        #msht-app-price
        #print names[0].contents[0].encode('utf-8')
        tmp=[" ".join(i.rsplit()) for i in names]
        names=tmp
        #print names
        prices=[i.find('div',{"class":"msht-app-price"}).find('span') for i in apps]
        prices=[i.contents[0].rsplit()[0] for i in prices]
        #print prices
        links=["https://cafebazaar.ir"+i.find('a')['href'].rsplit()[0] for i in apps]

        new_links = []
        for link in links:

            position = link.find('app/')
            position2 = link.find('?')

            new_links.append(link[position+4:position2-1])






        #print links
        #print names[0].encode('utf-8')
        #names,prices,links,imgs =====>inast:D
        dic = {}
        #print len(imgs),len(prices),len(links),len(names)
        for i in range(len(imgs)):
            dic[imgs[i]] = (names[i], prices[i], new_links[i])
        #print dic
        return render_template('results.html',data_dic = dic)

    return render_template('search.html')




@app.route('/categories')
def categories():
    return render_template('category.html')

@app.route('/cat/<cat>/?l=en&p=<page>',methods=["GET","POST"])
def showCat(cat,page):
    name=cat
    if cat not in ['word','trivia','strategy','sports-game','simulation','role-playing','racing','puzzle','music','family','educational','casual','board','arcade','adventure','action']:
        url="https://cafebazaar.ir/lists/"+cat+"-new-apps/?l=en&partial=true&p="+page
    else:
        url="https://cafebazaar.ir/lists/"+cat+"-new-games/?l=en&partial=true&p="+page
    def urlEncodeNonAscii(b):
        return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

    def iriToUri(iri):
        parts= urlparse.urlparse(iri)
        return urlparse.urlunparse(
            part.encode('idna') if parti==1 else urlEncodeNonAscii(part.encode('utf-8'))
            for parti, part in enumerate(parts)
        )
    #print url
    html=urllib.urlopen(url)
    soup=bs(html, 'lxml')
    bs()
    apps=soup.find_all('div',{"class":"msht-app"})
    #print type(apps)
    #print len(apps)
    apps=soup.findAll('div',{"class":"msht-app"})
    imgs=[i.find('img')['src'] for i in apps]

    #img= apps[0].find('img')
    #print img['src']
    names=[i.find('div',{"class":"msht-app-name"}).find('span') for i in apps]
    names=[i.contents[0] for i in names]
    #print names[0]
    #msht-app-price
    #print names[0].contents[0].encode('utf-8')
    tmp=[" ".join(i.rsplit()) for i in names]
    names=tmp
    #print names
    prices=[i.find('div',{"class":"msht-app-price"}).find('span') for i in apps]
    prices=[i.contents[0].rsplit()[0] for i in prices]
    #print prices
    links=["https://cafebazaar.ir"+i.find('a')['href'].rsplit()[0] for i in apps]

    new_links = []
    for link in links:

        position = link.find('app/')
        position2 = link.find('?')

        new_links.append(link[position+4:position2-1])
    #print links
    #print names[0].encode('utf-8')
    #names,prices,links,imgs =====>inast:D
    dic = {}
    #print len(imgs),len(prices),len(links),len(names)
    for i in range(len(imgs)):
        dic[imgs[i]] = (names[i], prices[i], new_links[i])
    #print dic
    return render_template('catresult.html',data_dic = dic, p=page , name=name)




@app.route('/contact')
def contaact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/application/<app_name>')
def application(app_name):

    url="https://cafebazaar.ir/app/" + app_name + "/?l=fa"
    html=urllib.urlopen(url)
    soup=bs(html, 'lxml')

    apps = soup.findAll('img',{"class":"app-img"})
    img = apps[0]['src']                                             #get image from cafe bazar

    apps = soup.findAll('div', {"class" : "app-name"})
    name = apps[0].find('h1').contents[0]                            #get app-name from cafe bazar

    apps = soup.findAll('div', {"class" : "dev"})
    co_name = apps[0].find('span').contents[0]

    apps = soup.findAll('span', {"class" : "pull-right"})
    category = apps[5].find('span').contents[0]
    number_of_install = apps[6].find('span').contents[0]
    size = apps[7].contents[2]
    version = apps[8].contents[0]

    dic = {}
    dic[img] = (name,co_name,category,number_of_install,size,version)

#<<<<<<< HEAD
    apps = soup.findAll('div', {"class" : "rtl"})
    print len(apps)
    experesions = apps[1].findAll('p')
    print (experesions)
    changes=soup.findAll('div',{"class" : "col-sm-12"})
    ch= changes[1].findAll('li')
    changes=[]
    for i in ch:
        changes+=i.contents
    print "done"


    return render_template('app.html', data_app = dic,img = img,ex = experesions ,change=changes)
#=======
    apps = soup.findAll('div', {"class" : " rtl "})
    exp = apps[0].find('p').contents[0]
    print exp



    return render_template('app.html', data_app = dic,img = img,ex = exp)
#>>>>>>> 752810dd36c15144a2a5a7f4c9ffabe1f3bf63f4


if __name__ == '__main__':
    app.run(debug=True)
