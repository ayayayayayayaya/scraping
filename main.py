import os
import sys
from urllib import request as req
from urllib import error
from urllib import parse
import bs4

def get_html(keyword):
    if not os.path.exists(keyword):
        os.mkdir(keyword)
    
    urlKey = parse.quote(keyword)
    url = 'https://www.google.com/search?hl=jp&q=' + urlKey + '&btnG=Google+Search&tbs=0&safe=off&tbm=isch'
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",}
    request = req.Request(url = url, headers = headers)
    page = req.urlopen(request)
    return page

def parse_img(page, keyword):
    html = page.read().decode('utf-8')
    html = bs4.BeautifulSoup(html, 'html.parser')
    elems = html.select('.rg_meta.notranslate')
    counter = 0
    for elem in elems:
        elem = elem.contents[0].replace('"','').split(',')
        elemdict = dict()
        for e in elem:
            num = e.find(':')
            elemdict[e[0:num]] = e[num + 1:]
        imgURL = elemdict['ou']
        
        print('get ' + imgURL)
        if '.jpg' in imgURL:
            ext = '.jpg'
        elif '.JPG' in imgURL:
            ext = '.JPG'
        elif 'png' in imgURL:
            ext = '.png'
        elif '.gif' in imgURL:
            ext = '.gif'
        elif '.jpeg;' in imgURL:
            ext = '.jpeg'
        else:
            ext = '.jpg'

        try:
            img = req.urlopen(imgURL)
            localfile = open('./' + keyword + '/' + keyword + str(counter) + ext, 'wb')
            localfile.write(img.read())
            img.close()
            localfile.close()
            counter += 1
        except UnicodeEncodeError:
            continue
        except error.HTTPError:
            continue
        except error.URLError:
            continue

def main():
    args = sys.argv
    keyword = args[1]
    page = get_html(keyword)
    parse_img(page, keyword)

if __name__ == '__main__':
    main()
