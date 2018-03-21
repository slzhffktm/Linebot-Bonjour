from PyLyrics import *

def lyrics(search):
    text = search.split(';')

    hasil = PyLyrics.getLyrics(text[0],text[1]);

    return str(hasil)