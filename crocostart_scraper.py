__author__ = 'ruio'

from bs4 import BeautifulSoup
import urllib2

url = 'http://crocostars.com/models.html'

if __name__ == '__main__':
    req = urllib2.urlopen(url)
    soup = BeautifulSoup(req)
    for div in soup.findAll('ul', {'class': 'profile-photos wrap'}):
        for h in soup.findAll('h4'):
            star_name = str(h.text).replace(' ', '-').lower()
            star_url = 'http://' + star_name + ".crocostars.com"
            print star_url
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
                            print 'http://img.crocostars.com/' + star_name + \
                                  '/' + '/'.join(album_name) + '/' + str(images['href']).replace('html', 'jpg')
