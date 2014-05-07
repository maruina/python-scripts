from bs4 import BeautifulSoup
import urllib2
import os, sys
import uuid
import requests
import time

# Subtract 1 to the desired limit
IMAGES_LIMIT = 9
ALBUM_LIMIT = 0

# Read the current working directory
basedir = os.getcwd()

main_url = 'http://crocostars.com/models'
url = 'http://crocostars.com/models.html'

timer = time.clock if sys.platform[:3] == 'win' else time.time


def get_image(img_url, file_name):
    r = requests.get(img_url)
    with open(str(file_name) + '.jpg', 'wb') as f:
        for chunk in r.iter_content(4096):
            f.write(chunk)


def parse_crocostar():
    # Create the script directory
    if not os.path.exists('scraper'):
        os.mkdir('scraper')
    os.chdir('scraper')
    
    start = timer()
    print '\nScript started at {}\n'.format(time.strftime("%c"))

    # For every page of the website
    for x in xrange(1, 96):
        if x is 1:
            current_url = url
        else:
            current_url = main_url + str(x) + '.html'

        req = urllib2.urlopen(current_url)
        soup = BeautifulSoup(req)

        # Find the HTML code with the list of all the actress
        div = soup.find('ul', {'class': 'profile-photos wrap'})
        # For every actress
        for actress in div.find_all('h4'):
            star_name = str(actress.text).replace(' ', '-').lower()
            if not os.path.exists(star_name):
                os.mkdir(star_name)
            else:
                print 'Actress {} already exists, skip'.format(actress.text)
                continue
            os.chdir(star_name)
            star_url = 'http://' + star_name + ".crocostars.com"
            print 'Scraping {} ...'.format(star_url)
            star_req = urllib2.urlopen(star_url)
            star_soup = BeautifulSoup(star_req)
            # Find the HTML code with the list of all the actress' album
            albums_div = star_soup.find('ul', {'class': 'profile-photos wrap'})
            for album_counter, album in enumerate(albums_div.find_all('a')):
                if album_counter > ALBUM_LIMIT:
                    break
                else:
                    print 'Scraping album {}'.format(album_counter)
                    album_name = str(album['href']).replace('http://crocostars.com/', '').split('/')[1:-1]
                    album_url = 'http://crocostars.com/' + star_name + '/' + '/'.join(album_name)
                    images_req = urllib2.urlopen(album_url)
                    images_soup = BeautifulSoup(images_req)
                    # Find the HTML code with the list of all the images in the current album
                    images_div = images_soup.find('ul', {'class': 'gals-list'})
                    for image_counter, image in enumerate(images_div.find_all('a')):
                        if image_counter > IMAGES_LIMIT:
                            break
                        else:
                            print '    Scraping image {}'.format(image_counter)
                            image_url = 'http://img.crocostars.com/' + star_name + \
                                        '/' + '/'.join(album_name) + '/' + str(image['href']).replace('html', 'jpg')
                            get_image(image_url, uuid.uuid4())
            print "Done, go to the next actress\n"
            os.chdir(os.path.join(basedir, 'scraper'))
    print "Script ended after {} minutes".format((timer() - start) / 60)

        

if __name__ == '__main__':
    parse_crocostar()
