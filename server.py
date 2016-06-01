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




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/search', methods=['GET', 'POST'])
def search():



    if request.method == 'POST':
        name = request.form['name']
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
            result="https://cafebazaar.ir/search/?q="+fkey+"&l=fa"
            return result
        url=search(name)
        html=urllib.urlopen(url)
        soup=bs(html, 'lxml')
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

    apps = soup.findAll('div', {"class" : "col-sm-4"})


    print category,version,size,install_number


    return render_template('app.html')


if __name__ == '__main__':
    app.run(debug=True)
