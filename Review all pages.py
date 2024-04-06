import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url):
    html_text=requests.get(url).text
    soul=BeautifulSoup(html_text,'lxml')
    reviews=soul.find_all('div',class_='body')
    
    review_names=[]
    names=[]
    dates=[]
    
    for review in reviews:
        review_name=review.find('h2',class_='text_header').text.strip()
        name=review.find('span').text.strip()
        date=review.find('time').text.strip()
        
        review_names.append(review_name)
        names.append(name)
        dates.append(date)
        
    return review_names,names,dates

base_url='https://www.airlinequality.com/airline-reviews/british-airways/page/{}'

review_names_all=[]
names_all=[]
dates_all=[]

page_number=1

while True:
    url=base_url.format(page_number)
    review_names,names,dates=scrape_page(url)
    if not review_names:
        break
    review_names_all.extend(review_names)
    names_all.extend(names)
    dates_all.extend(dates)
    page_number=page_number+1
    
data={'Review Name':review_names_all,
      'Names':names_all,
      'Dates':dates_all
      }

df_review=pd.DataFrame(data)
df_review.to_csv('Airline Review Details',index=False)