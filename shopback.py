#!/usr/bin/env python
# coding: utf-8

# In[195]:


import requests

from bs4 import BeautifulSoup
import pandas as pd
import json
import gspread
from datetime import date


# In[196]:


def update(value_df):
    sheet_id = '1x4A_IVSNKxa08qvViYp4KuG9Of7UuEbqcWllPk0i7fk'
    sheet_name = 'tripadvisor'
    gc = gspread.service_account('cred/travel_expense_credential.json')
    spreadsheet = gc.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    now_df = pd.DataFrame(worksheet.get_all_records())
    from_,to_ = now_df.shape
    from_cell = 'A'+str(from_+2)+':'+'D'+str(from_+1+value_df.shape[0])
    
    worksheet.update(from_cell, value_df.values.tolist())
    return print("successfully update")


# In[197]:


def get_rakuten():
    url = 'https://www.rakuten.com/tripadvisor.com?query=trip&position=2&type=suggest&store=12003'

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    raku_name = []
    raku_rate = []
    for i in soup.find_all('a',{'data-amp-evt-sig':"module_name,category_name,module_type"}):
        raku_name.append(i.find("span" ,{"class":"cb-cats-list-title"}).get_text())
        raku_rate.append(i.find("span",{"class":"cb-cats-list-amt cb"}).get_text())
    
    raku_df = pd.DataFrame(list(zip(raku_name,raku_rate)),columns=['name','rate'])
    raku_df["date"] = date.today().strftime('%Y-%m-%d')
    raku_df["rate"] = raku_df["rate"].apply(lambda x: float(x.strip('%'))*0.01)
    raku_df["source"] = 'Rakuten'
    return raku_df




# In[198]:





# In[199]:



def get_topcashback():
    url = 'https://www.topcashback.com/tripadvisor-hotels/'
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    name = []
    for i in soup.find_all('div',{"class":"gecko-small-text-wrap"}):
        name.append(i.get_text().strip())
    cash = []
    for i in soup.find_all('span',{"class":"cashback-desc"}):
        cash.append(i.get_text().strip())
    df = pd.DataFrame(list(zip(name,cash)),columns=['name','rate'])
    df["date"] = date.today().strftime('%Y-%m-%d')
    df["source"] = 'Topcashback'
    df = df[df.name!= 'TripAdvisor Plus Subscription']
    df["rate"] = df["rate"].apply(lambda x: float(x.strip('%'))*0.01)
    df = df.reset_index(drop=True)
    return df


# In[200]:





# In[ ]:


if __name__ == '__main__':
    raku_df = get_rakuten()
    update(raku_df)
    topcash_df = get_topcashback()
    update(topcash_df)

