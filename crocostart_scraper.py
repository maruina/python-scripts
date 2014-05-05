__author__ = 'ruio'

from bs4 import BeautifulSoup
import urllib2
import os

# Read the current working directory
basedir = os.getcwd()

main_url = 'http://crocostars.com/models'
url = 'http://crocostars.com/models.html'

if __name__ == '__main__':
    # Create the script directory
    os.mkdir('scraper')
    os.chdir('scraper')
    for x in xrange(1, 96):
        if x is 1:
            current_url = url
        else:
            current_url = main_url + str(x) + '.html'
        req = urllib2.urlopen(current_url)
        soup = BeautifulSoup(req)
        for div in soup.findAll('ul', {'class': 'profile-photos wrap'}):
            for h in soup.findAll('h4'):
                star_name = str(h.text).replace(' ', '-').lower()
                os.mkdir(star_name)
                os.chdir(star_name)
                star_url = 'http://' + star_name + ".crocostars.com"
                print 'Scraping {}'.format(star_url)
                star_req = urllib2.urlopen(star_url)
                star_soup = BeautifulSoup(star_req)
                for star_div in star_soup.findAll('ul', {'class': 'profile-photos wrap'}):
                    for album in star_div.findAll('a'):
                        album_name = str(album['href']).replace('http://crocostars.com/', '').split('/')[1:-1]
                        album_url = 'http://crocostars.com/' + star_name + '/' + '/'.join(album_name)
                        images_req = urllib2.urlopen(album_url)
                        images_soup = BeautifulSoup(images_req)
                        for images_div in images_soup.findAll('ul', {'class': 'gals-list'}):
                            for images in images_div.findAll('a'):
                                # print 'http://img.crocostars.com/' + star_name + \
                                #       '/' + '/'.join(album_name) + '/' + str(images['href']).replace('html', 'jpg')
                                v = 1
                os.chdir(os.path.join(basedir, 'scraper'))
