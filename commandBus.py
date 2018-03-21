#from command.lirik import lyrics
from PyLyrics import *
import psycopg2

from bs4 import BeautifulSoup as bs
import requests

import random
from random import randrange

def lyrics(search):
    text = search.split(';')
    try:
        hasil = PyLyrics.getLyrics(text[0],text[1])    
    except:
        hasil = 'Sorry, no lyrics for this song.'
    
    return (hasil)

def resolve(text):
    textsplit = text.split(' ',1)
    greet = ['bonjour','hello','hi','halo']
    if textsplit[0] in greet:
        return 'greeting'
    elif text == 'leave sana':
        return 'leave'
    elif 'apakah' in text:
        ans = ['ya','tidak','mungkin'] #list jawaban
        idx = randrange(0,len(ans))
        return ans[idx]
    elif text == '#jadwal':
        return 'jadwal'
    elif textsplit[0]=='#lyric':
        hasil = lyrics(textsplit[1])
        text = str(hasil)
        textsplit = text.split('<br>')
        hasil = ''
        for te in textsplit:
            hasil = hasil + te +'\n'
        
        return str(hasil)
    elif textsplit[0] == '#weather':
        weather = weatherForecast(textsplit[1])
        return str(weather)

def getLink(text):
    name = text[6:]
    url = "http://theapache64.xyz:8080/movie_db/search?keyword=" + name
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers)
    soup = bs(response.text, 'html.parser')
    data = soup.text.split('"');

    #getImageLink
    i = data.index('poster_url') + 2
    return data[i]

def getMovieData(text):
    name = text[6:]
    url = "http://theapache64.xyz:8080/movie_db/search?keyword=" + name
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers)
    soup = bs(response.text, 'html.parser')
    data = soup.text.split('"');

    i = data.index('name')+2
    title = 'Title : ' + data[i]

    i = data.index('rating') +2
    rating = 'Rating : ' + data[i]

    i = data.index('plot')+2
    overview = 'Overview : ' + data[i]

    movie = title + '\n' + rating + '\n \n' + overview

    return movie


def insert(index, mainstring, insertstring):
    return mainstring[:index] + insertstring + mainstring[index:]

# weather
def weatherForecast(when):
    url = 'http://www.bmkg.go.id/cuaca/prakiraan-cuaca.bmkg?Kota=Bandung&AreaID=501212&Prov=10'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers)
    soup = bs(response.text, 'html.parser')

    if when == 'today':
        temp = soup.find(id='TabPaneCuaca2').find(class_='row no-space-carousel-block')
        day = temp.find_all(class_='col-md-3')
        i = 4
        while day == []:
            string = 'col-md-' + str(i)
            day = temp.find_all(class_= string)
    elif when == 'tomorrow':
        day = soup.find(id='TabPaneCuaca3').find(class_='row no-space-carousel-block').find_all(class_='col-md-3')

    weather = []

    for td in day:
        time = td.find(class_='kota').get_text()
        sky = td.find(class_='kiri').get_text().replace('\n','')
        kanan = td.find(class_='kanan')
        heading = kanan.find(class_='heading-md').get_text()

        texts = kanan.findAll('p')
        texts = [t.get_text() for t in texts]
        texts = [t.replace('\xa0','').replace('&degC',heading[2:]) for t in texts]
    
        tempwind = texts[0].split(';')

        temperature = [heading, tempwind[0], tempwind[1]]   #[0] header [1] down [2] up [3] raindrops
        raindrops = tempwind[2]

        windspeed = insert(texts[1].find('am',4)+2, texts[1], ' ')

        text = time + ':\n' + sky + '\n' + temperature[0] + '  ⤵' + temperature[1] + '  ⤴' + temperature[2] + '\n☂ Precipitation: ' + raindrops + '\nWindspeed: ' + windspeed
        weather.append(text)
    
    reply = ''
    for i in range(len(weather)):
        if i != len(weather)-1:
            reply += weather[i] + '\n\n'
        else:
            reply += weather[i]

    return reply

def toDoList(what):
    
    DATABASE = "host='ec2-54-225-88-199.compute-1.amazonaws.com' dbname='d5ro04p9mlsrdm' user='qnjhdetjclkucm' password='9b2817186607e65619f4f7925ceb5a377e7cee7d0c6927df6ee974705de9270f'"
    conn = psycopg2.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS jadwal (date DATE(), todo VARCHAR(50))")


