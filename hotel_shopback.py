#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests

from bs4 import BeautifulSoup
import pandas as pd
import json
import gspread
from datetime import date


# In[135]:


def update(value_df,sheet_name):
    sheet_id = '1x4A_IVSNKxa08qvViYp4KuG9Of7UuEbqcWllPk0i7fk'
    #sheet_name = 'hotel'
    gc = gspread.service_account('travel_expense_credential.json')
    spreadsheet = gc.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    now_df = pd.DataFrame(worksheet.get_all_records())
    from_,to_ = now_df.shape
    from_cell = 'A'+str(from_+2)+':'+'D'+str(from_+1+value_df.shape[0])
    
    worksheet.update(from_cell, value_df.values.tolist())
    return print("successfully update")


# In[136]:


def get_all_hotels_rakuten():
    all_h = []
    all_h_name = []
    url = 'https://www.rakuten.com/marriotthotelsandresorts.com?query=marriot'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    number = soup.find('a',{"class":"cb prox-b nohover"}).get_text()
    number = number[:number.find('%')+1]
    all_h.append(number)
    all_h_name.append('Marriott')
    
    url_ihg = 'https://www.rakuten.com/ihg.com?query=ihg'
    page_ihg = requests.get(url_ihg)
    soup_ihg = BeautifulSoup(page_ihg.text,'html.parser')

    ihg = soup_ihg.find('a',{"class":"cb prox-b nohover"}).get_text()
    ihg = ihg[:ihg.find('%')+1]
    all_h.append(ihg)
    all_h_name.append('Ihg')
    
    url_hilton = 'https://www.rakuten.com/hilton.com?query=hilton'
    page_hilton = requests.get(url_hilton)
    soup_hilton = BeautifulSoup(page_hilton.text, 'html.parser')
    

    for i in soup_hilton.find_all('span',{"class":"cb-cats-list-amt"}):
        if i.get_text() != 'Cash Back':
            all_h.append(i.get_text())
    
    for i in soup_hilton.find_all('span',{"class":"cb-cats-list-title"}):
        if i.get_text() != 'Categories':
            all_h_name.append('Hilton - '+i.get_text())

    
    raku_hotel_df = pd.DataFrame(list(zip(all_h_name,all_h)),columns=['name','rate'])
    raku_hotel_df["date"] = date.today().strftime('%Y-%m-%d')
    raku_hotel_df["source"] = 'Rakuten'
    raku_hotel_df["rate"] = raku_hotel_df["rate"].apply(lambda x: float(x.strip('%'))*0.01)
    return raku_hotel_df
            


# In[137]:



def get_all_hotel_agency_rakuten():
    agency_name = []
    agency_ratio = []
    
    booking_url = 'https://www.rakuten.com/booking.com'
    booking_page = requests.get(booking_url)
    booking_soup = BeautifulSoup(booking_page.text, 'html.parser')
    
    booking_number = booking_soup.find('a',{"class":"cb prox-b nohover"}).get_text()
    booking_number = booking_number[:booking_number.find('%')+1]
    agency_ratio.append(booking_number)
    agency_name.append('Booking.com')
    
    agoda_url = 'https://www.rakuten.com/agoda.com'
    agoda_page = requests.get(agoda_url)
    agoda_soup = BeautifulSoup(agoda_page.text, 'html.parser')
    
    agoda_number = agoda_soup.find('a',{"class":"cb prox-b nohover"}).get_text()
    agoda_number = agoda_number[:agoda_number.find('%')+1]
    agency_ratio.append(agoda_number)
    agency_name.append('Agoda')
    
    

    hotel_url = 'https://www.rakuten.com/hotels.com'
    hotel_page = requests.get(hotel_url)
    hotel_soup = BeautifulSoup(hotel_page.text,'html.parser')

    for i in hotel_soup.find_all('span',{"class":"cb-cats-list-amt"}):
        if i.get_text() != 'Cash Back':
            agency_ratio.append(i.get_text())
    
    for i in hotel_soup.find_all('span',{"class":"cb-cats-list-title"}):
        if i.get_text() != 'Categories':
            agency_name.append('Hotels.com - '+i.get_text())

    
    raku_hotel_agency_df = pd.DataFrame(list(zip(agency_name,agency_ratio)),columns=['name','rate'])
    raku_hotel_agency_df["date"] = date.today().strftime('%Y-%m-%d')
    raku_hotel_agency_df["source"] = 'Rakuten'
    raku_hotel_agency_df["rate"] = raku_hotel_agency_df["rate"].apply(lambda x: float(x.strip('%'))*0.01)
    return raku_hotel_agency_df
    


# In[138]:


def get_all_hotel_agency_topcashback():
    agency_name = []
    agency_ratio = []
    
    booking_url = 'https://www.topcashback.com/booking-com/'
    booking_page = requests.get(booking_url)
    booking_soup = BeautifulSoup(booking_page.text, 'html.parser')

    booking_number = booking_soup.find('span',{"class":"cashback-desc"}).get_text()

    agency_name.append('Booking.com')
    agency_ratio.append(booking_number)

    agoda_url = 'https://www.topcashback.com/agoda/'
    agoda_page = requests.get(agoda_url)
    agoda_soup = BeautifulSoup(agoda_page.text, 'html.parser')
    
    agoda_number = agoda_soup.find('span',{"class":"cashback-desc"}).get_text()

    agency_name.append('Agoda')
    agency_ratio.append(agoda_number)

    hotel_url = 'https://www.topcashback.com/hotels-com/'
    hotel_page = requests.get(hotel_url)
    hotel_soup = BeautifulSoup(hotel_page.text, 'html.parser')

    hotel_number = hotel_soup.find('span',{"class":"cashback-desc"}).get_text()

    agency_name.append('Hotels.com - All Other Bookings')
    agency_ratio.append(hotel_number)

    
    topcash_hotel_agency_df = pd.DataFrame(list(zip(agency_name,agency_ratio)),columns=['name','rate'])
    topcash_hotel_agency_df["date"] = date.today().strftime('%Y-%m-%d')
    topcash_hotel_agency_df["source"] = 'Topcashback'
    topcash_hotel_agency_df["rate"] = topcash_hotel_agency_df["rate"].apply(lambda x: float(x.strip('%'))*0.01)
    return topcash_hotel_agency_df


# In[139]:


def get_all_hotels_topcashback():
    hotel_name = []
    hotel_ratio = []

    marriott_url = 'https://www.topcashback.com/marriott-international/'
    marriott_page = requests.get(marriott_url)
    marriott_soup = BeautifulSoup(marriott_page.text, 'html.parser')

    marriott_number = marriott_soup.find('span',{"class":"cashback-desc"}).get_text()
    
    hotel_name.append('Marriott')
    hotel_ratio.append(marriott_number)
    
    ihg_url = 'https://www.topcashback.com/ihg/'
    ihg_page = requests.get(ihg_url)
    ihg_soup = BeautifulSoup(ihg_page.text, 'html.parser')
    
    ihg_number = ihg_soup.find('span',{"class":"cashback-desc"}).get_text()
    hotel_name.append('Ihg')
    hotel_ratio.append(ihg_number)
    
    
    hilton_url = 'https://www.topcashback.com/hilton/'
    hilton_page = requests.get(hilton_url)
    hilton_soup = BeautifulSoup(hilton_page.text, 'html.parser')
    hilton = []
    for i in hilton_soup.find_all('div',{"class":"gecko-small-text-wrap"}):
        hilton.append((i.get_text().strip()))
    hilton_ratio = []
    for i in hilton_soup.find_all('span',{"class":"cashback-desc"}):
        hilton_ratio.append(i.get_text()) 
        

    for i in list(zip(hilton,hilton_ratio)):
        if i[0] =='Non HHonors Members and Blue HHonors Members - All Properties':
            hotel_name.append('Hilton - Blue Member Hotel Stay')
            hotel_name.append('Hilton - Non-Member Hotel Stay')
            hotel_ratio.extend([i[1],i[1]])
        if i[0] =='All Other HHonors Members':
            hotel_name.append('Hilton - Diamond Member Hotel Stay')
            hotel_name.append('Hilton - Gold Member Hotel Stay')
            hotel_name.append('Hilton - Silver Member Hotel Stay')
            hotel_ratio.extend([i[1],i[1],i[1]])
    
    topcash_hotel_df = pd.DataFrame(list(zip(hotel_name,hotel_ratio)),columns=['name','rate'])
    topcash_hotel_df["date"] = date.today().strftime('%Y-%m-%d')
    topcash_hotel_df["source"] = 'Topcashback'
    topcash_hotel_df["rate"] = topcash_hotel_df["rate"].apply(lambda x: float(x.strip('%'))*0.01)
    return topcash_hotel_df


# In[ ]:


if name = '__main__':
    hotel_rakuten = get_all_hotels_rakuten()
    update(hotel_rakuten,'hotel')

    hotel_topcashback = get_all_hotels_topcashback()
    update(hotel_topcashback,'hotel')
    
    agency_rakuten = get_all_hotel_agency_rakuten()
    update(agency_rakuten,'agency')

    agency_topcashback = get_all_hotel_agency_topcashback()
    update(agency_topcashback,'agency')

