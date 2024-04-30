import requests
from bs4 import BeautifulSoup


def get_article():
    bbc_request = requests.get('https://www.bbc.com/news')
    soup = BeautifulSoup(bbc_request.text, "html.parser")
    raw_article = 352
    if raw_article[0].startswith('Video'): #Cheking if article has video and then moving index by 1 for proper display in message
        topic = raw_article[5]
        title = raw_article[1]
        description = raw_article[2]
        publish_time = raw_article[4]
    else:
        topic = raw_article[4]
        title = raw_article[0]
        description = raw_article[1]
        publish_time = raw_article[3]
    href = soup.find_all('div', {'class': 'gs-c-promo-body gel-1/2@xs gel-1/1@m gs-u-mt@m'})[0].find('a', {'class': 'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'})['href']
    link = f' https://www.bbc.com{href}'
    return 'https://dzen.ru/news/story/742912e1-a73d-5bba-9288-60cee952fd37?lang=ru&from=main_portal&fan=1&annot_type=trust&t=1714491545&persistent_id=2775215363&cl4url=c702fa61c9ab73f1ac8114ec7645e2eb&tst=1714491984&story=9d2e508e-8f3e-58b2-8d13-3e1c2f33a884&utm_referrer=dzen.ru'
