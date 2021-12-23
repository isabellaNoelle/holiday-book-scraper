import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

print('Starting: Holiday Book Scraper')

ua_num = 0
ua_list = ['Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
           'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
           'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
           'Mozilla/5.0 (compatible; MJ12bot/v1.4.5; http://www.majestic12.co.uk/bot.php?+)',
           'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)'
           ]

HEADERS = ({'User-Agent': ua_list[ua_num],
            'Accept-Language': 'en-US, en;q=0.5'})


# FUNCTIONS
def easy_links(res, holiday: str) -> None:
    for a_tag in res:
        if 'Audible' in a_tag.text or 'free trial' in a_tag.text:
            continue
        book_links[a_tag['href']] = holiday


def fig_links(res, holiday: str) -> None:
    for fig in res:
        link = fig.find('a')
        if link is None:
            continue
        if 'amazon' in link['href']:
            book_links[link['href']] = holiday


# Extra books
book_links = {'https://www.amazon.com/Cajun-Night-Before-Christmas%C2%AE-Christmas/dp/0882899406/ref=sr_1_1?keywords'
              '=cajun+christmas+book&qid=1638921453&sr=8-1': 'Christmas'}

# Thanksgiving book list
print('Starting: Book list scraping')
print('On: Thanksgiving list')
th_url = 'https://parentingchaos.com/thanksgiving-books-for-kids/'
th_page = requests.get(th_url, headers=HEADERS)
th_soup = BeautifulSoup(th_page.content, 'html.parser')
th_figs = th_soup.find_all('h3', class_='elementor-heading-title elementor-size-default')
fig_links(th_figs, 'Thanksgiving')

# Hanukkah book list
print('On: Hanukkah list')
hh_url = 'https://www.familyeducation.com/fun/hanukkah/10-best-hanukkah-books-kids'
hh_page = requests.get(hh_url, headers=HEADERS)
hh_soup = BeautifulSoup(hh_page.content, 'html.parser')
hh_a = hh_soup.find_all('a', href=re.compile('amazon'))
easy_links(hh_a, 'Hanukkah')

# Kwanzaa book list
print('On: Kwanzaa list')
kw_url = 'https://www.familyeducation.com/the-10-best-kwanzaa-books-for-kids'
kw_page = requests.get(kw_url, headers=HEADERS)
kw_soup = BeautifulSoup(kw_page.content, 'html.parser')
kw_a = kw_soup.find_all('a', href=re.compile('amazon'))
easy_links(kw_a, 'Kwanzaa')

# Christmas 100+ book list
print('On: Christmas list')
ch_url = 'https://theeducatorsspinonit.com/100-christmas-books-every-child-should/'
ch_page = requests.get(ch_url, headers=HEADERS)
ch_soup = BeautifulSoup(ch_page.content, 'html.parser')
ch_figs = ch_soup.find_all('figure', class_='aligncenter')
fig_links(ch_figs, 'Christmas')

# New Years book list
print('On: New Years list')
ny_url = 'https://www.thebutterflyteacher.com/happy-new-years-books-for-kids/'
ny_page = requests.get(ny_url, headers=HEADERS)
ny_soup = BeautifulSoup(ny_page.content, 'html.parser')
ny_a = ny_soup.find_all('a', attrs={'aria-label': True, 'href': re.compile('amzn.to')})
easy_links(ny_a, 'New Years')

print(f'There are {len(book_links)} books to scrape!')
print('Finished: Book list scraping')

# get info from all Amazon book links
print('Starting: Amazon book scraping')
all_books = []
for bl in book_links.keys():
    book_page = requests.get(bl, headers=HEADERS)
    book_soup = BeautifulSoup(book_page.content, 'html.parser')
    if book_soup.find(id='productTitle') is None:
        ua_num += 1
        try:
            HEADERS['User-Agent'] = ua_list[ua_num]
        except IndexError:
            print('RAN OUT OF USER AGENTS. TRY SCRAPING AGAIN TOMORROW')
            quit()
        book_page = requests.get(bl, headers=HEADERS)
        book_soup = BeautifulSoup(book_page.content, 'html.parser')

    # title
    title = book_soup.find(id='productTitle')
    try:
        title = title.text.strip()
    except AttributeError:
        print(f'Trouble scraping title for {bl}')
        title = None

    # authors
    author = ''
    byline = book_soup.find(id='bylineInfo')
    try:
        byline = byline.find_all('span', class_='author')
        for by in byline:
            if by.find('div', class_='a-popover-preload') is not None:
                a = by.find('span', class_='a-size-medium')
                author += ' ' + a.text.strip()
                continue
            a = by.find('a')
            c = by.find('span', class_='a-color-secondary')
            author += ' ' + a.text.strip() + ' ' + c.text.strip()
        author = author.lstrip()
    except AttributeError:
        author = None
        print(f'Trouble scraping authors for {bl}')

    # rating & reviews
    try:
        rating_chunk = book_soup.find(id='averageCustomerReviews')
        reviews = rating_chunk.find(id='acrCustomerReviewText')
        reviews = reviews.text.split(' ', 1)[0]
        reviews = int(reviews.strip().replace(',', ''))
        rating = rating_chunk.find(class_='a-icon-alt')
        rating = rating.text.split(' ', 1)
        rating = float(rating[0])
    except AttributeError:
        print(f'Trouble scraping ratings for {bl}')
        rating = None
        reviews = None

    # prices
    kindle_price = None
    paper_price = None
    hardcover_price = None

    price_list = book_soup.find('ul', class_='a-unordered-list a-nostyle a-button-list a-horizontal')
    try:
        price_list = price_list.find_all('li', class_='swatchElement')
        for p in price_list:
            p_act = p.find('span', string=re.compile(r'\$'))
            try:
                p_act = p_act.text.split('$')[-1]
                p_act = float(p_act.strip())
                p_type = p.find('span', class_=False)
                if p_type.text == 'Kindle':
                    kindle_price = p_act
                elif p_type.text == 'Hardcover':
                    hardcover_price = p_act
                else:
                    paper_price = p_act
            except AttributeError:
                continue
    except AttributeError:
        print(f'Trouble scraping prices for {bl}')

    # main data
    book_dict = {
        'link': bl,
        'holiday': book_links[bl],
        'title': title,
        'author': author,
        'rating': rating,
        'reviews': reviews,
        'kindle price': kindle_price,
        'paperback price': paper_price,
        'hardcover price': hardcover_price
    }

    # extras
    extras_list = book_soup.find(id='richProductInformation_feature_div')
    try:
        extras_list = extras_list.find('ol', class_='a-carousel')
        extras_list = extras_list.find_all('li', class_='a-carousel-card rpi-carousel-attribute-card')
        for extra in extras_list:
            # label
            label = extra.find('div', class_='a-section a-spacing-small a-text-center rpi-attribute-label')
            label = label.find('span')
            label = label.text.strip()
            # content
            content = extra.find('div', class_='a-section a-spacing-none a-text-center rpi-attribute-value')
            content = content.find('span')
            content = content.text.strip()

            book_dict[label] = content
    except AttributeError:
        continue

    all_books.append(book_dict)

print('Finished: Amazon book scraping')

books_df = pd.DataFrame(all_books)
books_df.to_csv('holiday_books.csv', index=False)

print('Finished: Holiday Book Scraper')
