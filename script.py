import csv
import newspaper
from newspaper import Article
import datetime
import numpy as np
import pandas as pd

file = open("/home/hosni/Desktop/Google_News_Crawling/venv/Donald trump_2019-05-01_SearchGoogleNews.csv", "r")
test = csv.reader(file)
liste_url = []
for row in test:
    liste_url.append(row[1])
New_liste = liste_url[1:]
print("La liste des URL est :", New_liste)
print("Nombre des URL est: ", len(New_liste))

date = str(datetime.datetime.now().date())
# csv filename
filename = "HTML_CONTENT_" + date + '_NLP.txt'
f = open(filename, "at")

for i in New_liste:
    article = Article(i)
    article.download()
    f.write(article.html)
f.close()

df=[]
filename2 = "Metadata_" + date +".csv"
f2 = open(filename2,"w")
for j in New_liste:
    try:
        articl = Article(j)
        articl.download()
        articl.parse()
    except:
        print('***FAILED TO DOWNLOAD***', articl.url)
        continue
    df = np.append(df, [str(articl.title)
        , str(articl.extractor)
        , str(articl.authors)
        , str(articl.publish_date)])
    df = np.reshape(df, (-1, 4))

df1 = pd.DataFrame(df, columns=['Title', 'Extractor', 'Authors', 'Publish_Date'])
df1.to_csv(f2, index=False, encoding='utf-8')