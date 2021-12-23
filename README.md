# Holiday Book Scraper
Web scraper built to scrape holiday book lists and Amazon book/product pages for winter holiday book data. Made with 
Python. As it is now, it scrapes data for just under 200 books (over 100 of those are Christmas books).

## Requirements
- requests
- pandas
- bs4
- jupyter (optional - if you want to view the .ipynb file)

## Files
- main.py
  - Script for the web scraper. This script scrapes book lists for links to children's books about Thanksgiving, 
  Hanukkah, Kwanzaa, Christmas, and New Years. It then uses those links to scrape book/product information from the 
  individual Amazon pages and outputs the data to a csv file.
- Christmas Book Web Scraping.ipynb
  - This file was used for scratch but is mostly empty now
- holiday_books.csv
  - csv output from the main.py script

## Extra
I had to use several web scraping/crawler user agents to get the Amazon data. Those user agents were pulled from this 
WhatIsMyBrowser.com list: [Crawler User Agents](https://developers.whatismybrowser.com/useragents/explore/software_type_specific/crawler/).
### Also...
- [BeautifulSoup (bs4) documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)
- [Requests for Humans Documentation](https://docs.python-requests.org/en/latest/)
- [Thanksgiving Books for Kids](https://parentingchaos.com/thanksgiving-books-for-kids/)
- [10 Best Hanukkah Books for Kids](https://www.familyeducation.com/fun/hanukkah/10-best-hanukkah-books-kids)
- [The 10 Best Kwanzaa Books for Kids](https://www.familyeducation.com/the-10-best-kwanzaa-books-for-kids)
- [100 Christmas Books Every Child Should Read Before They Turn 10](https://theeducatorsspinonit.com/100-christmas-books-every-child-should/)
    - This page actually has links for ~120 books
- [Happy New Years Books for Kids](https://www.thebutterflyteacher.com/happy-new-years-books-for-kids/) 
