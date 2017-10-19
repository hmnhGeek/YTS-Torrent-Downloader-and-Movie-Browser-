import requests as req
from bs4 import BeautifulSoup as bs
import os, json

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def browse(movie):

    # build the urls.
    base_url = 'https://yts.ag/browse-movies'
    url = '{}/'.format(base_url) + movie

    # send a get request for the movie.
    r = req.get(url)
    # make a soup
    soup = bs(r.text)

    movies_found = []
    count = 0

    # find the div tags having movies.
    for div in soup.findAll('div', attrs = {'class':'browse-movie-bottom'}):
        a = div.find('a')
        movies_found.append(a)

    for movie in movies_found:
        print count+1, movie.text
        count += 1

    print
    print "Select a movie!!"
    print
    srno = input()

    if srno > 0 and srno <= len(movies_found):

        #get the index of the movie
        index = srno - 1

        selected_movie = movies_found[index]
        print "Movie selected: "+selected_movie.text
        print selected_movie.attrs['href']

        # make a new soup.
        movieSoup = bs(req.get(selected_movie.attrs['href']).text)

        return movieSoup

    else:
        print "Wrong Choice!!"

        chose_again = raw_input("Chose again? (y/n) ").upper()
        if chose_again == 'Y':
            browse(movie)

        return None

def getinfo(movie):

    soup = browse(movie)

    # movie name
    h1 = soup.find('h1')
    name = h1.text

    h2 = soup.findAll('h2')
    # movie year
    year = h2[0].text

    # movie type
    typ = h2[1].text

    # getting the likes.
    span = soup.find('span', attrs = {'id':'movie-likes'})
    likes = span.text

    # getting IMDb rating.
    rating = soup.find('span', attrs = {'itemprop':'ratingValue'})
    imdb_rating = rating.text

    # Getting director
    direc = soup.find('span', attrs = {'itemprop':'director'})
    director = direc.text

    # actors list
    actors_tag = soup.findAll('span', attrs = {'itemprop':'actor'})
    actors = [i.text for i in actors_tag]

    # getting synopsis
    synop = soup.find('p', attrs = {'class':'hidden-sm hidden-md hidden-lg'})
    synopsis = synop.text

    data = {
            'name': name,
            'release_year': year,
            'type': typ,
            'likes': likes,
            'imdb_rating': imdb_rating,
            'director': director,
            'actors': actors,
            'synopsis': synopsis
        }

    data = json.dumps(data)

    return json.loads(data)

def download_torrent(movie, location = None):

    parent = os.getcwd()
    
    soup = browse(movie)
    counter = 0
    download_options = []
    
    if location != None:
        if not os.path.isdir(location):
            os.mkdir(location)

        os.chdir(location)

    if not os.path.isdir(movie+' torrent'):
        os.mkdir(movie+' torrent')

    os.chdir(movie+' torrent')

    # find the download buttons (links).
    for a in soup.findAll('a', attrs = {'class':'download-torrent button-green-download2-big'}):
        download_options.append(a)
        print counter+1, a.attrs['title']

        counter += 1

    # now ask the user to select a torrent file. Whether 3D, 720p or 1080p.
    torr_format = input("Srno of the torrent to download: ")

    if torr_format in range(1, len(download_options)+1):
        # get the index
        index = torr_format - 1

        # get that anchor tag
        a_tag = download_options[index]

        link = a.attrs['href']

        # download the torrent file.
        name_of_torrent_file = os.path.basename(link)

        with open(name_of_torrent_file+'.torrent', 'wb') as f:
            f.write(req.get(link).content)

        print "Downloaded!!"

    else:
        print "Wrong Choice!!"

        chose_again = raw_input("Chose again? (y/n) ").upper()
        if chose_again == 'Y':
            download_torrent(movie, location)

    os.chdir(parent)

def movie_info(movie):
    d = getinfo(movie)
    print '\n'*3
    for i in d:
        print i, '\t\t', d[i]
        print
