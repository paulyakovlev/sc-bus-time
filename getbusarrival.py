# Python program to scrape website
# and save quotes from website
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

URL = "https://www.scmtd.com/en/stop/1232#tripDiv"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')

table = soup.find('table', attrs = {'class':'metrotable'}) 

new_table = pd.DataFrame(columns=range(0,6), index = range(0,20)) # I know the size 

row_marker = 0
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        new_table.iat[row_marker,column_marker] = column.get_text()
        column_marker += 1
    row_marker +=1

print(new_table)

