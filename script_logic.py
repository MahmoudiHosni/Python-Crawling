from io import open
import requests
from bs4 import BeautifulSoup
import time
import datetime
from random import randint
import numpy as np
import pandas as pd


query2Google = input("What do you looking for from Google News?\n")


def QGN(query2Google):
    # Keywords for query
    s = '"' + query2Google + '"'
    s = s.replace(" ", "+")
    # timestamp
    date = str(datetime.datetime.now().date())
    # csv filename
    filename = query2Google + "_" + date + "_" + 'SearchGoogleNews.csv'
    f = open(filename, "wb")
    url = "https://news.google.com/search?q=" + s + "&hl=en-US&gl=US&ceid=US:en"
    time.sleep(randint(0, 2))  # waiting

    htmlpage = requests.get(url)
    print("Status code: " + str(htmlpage.status_code))
    soup = BeautifulSoup(htmlpage.text, 'lxml')

    df = []
    for result_table in soup.findAll("div", {"class": "xrnccd"}):
        a_click = result_table.find("a")
        #print ("-----Title----\n" + str(result_table.find("a", {"class": "DY5T1d"}).renderContents()))#Title

        #print ("----URL----\n" + "https://news.google.com"+str(a_click.get("href"))) #URL

        #print ("----Brief----\n" + str(result_table.find("p", {"class": "HO8did Baotjf RD0gLb"}).renderContents()))#Brief

        #print ("Done")
        df = np.append(df, [str(result_table.find("a", {"class": "DY5T1d"}).renderContents()).strip("b")
            , "https://news.google.com"+str(a_click.get("href")).strip('/url?q=')
            ,str(result_table.find("p", {"class": "HO8did Baotjf RD0gLb"}).renderContents()).strip("b").strip("...")])

        df = np.reshape(df, (-1, 3))
        df1 = pd.DataFrame(df, columns=['Title', 'URL', 'Brief'])
    print("Search Crawl Done!")

    df1.to_csv(filename, index=False, encoding='utf-8')
    f.close()



QGN(query2Google)

