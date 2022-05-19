# Library/module imports
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
import pandas as pd

# Variables: 
dates = []
urls = []
final = []
url = 'https://spotifycharts.com/regional/no/daily/'
start_date = datetime(2022, 3, 1)
end_date = datetime(2022, 5, 1)
delta = end_date - start_date

# print(delta.days+1)

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    day_string = day.strftime('%Y-%m-%d')
    dates.append(day_string)


def add_url():
    for date in dates:
        c_string = url + date
        urls.append(c_string)


add_url()


def song_scrape(x, songs):
    pg = x
    for tr in songs.find("tbody").findAll("tr"):
        artist = tr.find("td", {"class": "chart-table-track"}).find("span").text
        artist = artist.replace("by ", "").strip()

        rank= tr.find('td',{'class':'chart-table-position'}).text
        title = tr.find("td", {"class": "chart-table-track"}).find("strong").text
        songid = tr.find("td", {"class": "chart-table-image"}).find("a").get("href")
        songid = songid.split("track/")[1]
        url_date = x.split("daily/")[1]
        final.append([rank,title, artist, songid, url_date])


# Avoid http 403 forbidden error with this code: 

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

for u in urls:
    read_pg = requests.get(u, headers=header)
    sleep(2)
    # return read_pg.status_code
    soup = BeautifulSoup(read_pg.text, "html.parser")

    # Using BeautifulSoup, we're getting the specific data from the HTML:
    # There is only 1 table = which is the table with the data to extract:
    songs = soup.findAll("table")[0]

    # Call "song_scrape" function to retrieve the data from the table:
    song_scrape(u, songs)

final_df = pd.DataFrame(final, columns=['Rank',"Title", "Artist", "Song ID", "Chart Date"])

final_df['Code'] = 'NOR'

# print(final_df) # Print the dataframe, if you want

with open('nor.csv', 'w',encoding="utf-8") as f:
    final_df.to_csv(f, header=True, index=False)