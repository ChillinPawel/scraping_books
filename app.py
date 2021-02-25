import logging
import aiohttp
import async_timeout
import asyncio
import time

from pages.books_page import BooksPage

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    filename='logs.txt')

logger = logging.getLogger('scraping')


async def fetch_page(session, url):
    page_start = time.time()
    async with async_timeout.timeout(20):
        async with session.get(url) as response:
            logger.info(f'Page took {time.time() - page_start} to load')
            return await response.text()


async def get_multiple_pages(loop, *urls):
    async with aiohttp.ClientSession(loop=loop) as session:
        pages = [fetch_page(session, url) for url in urls]
        grouped_pages = await asyncio.gather(*pages)
        return grouped_pages


# new way with asyncio
logger.debug('Creating asyncio loop')
loop = asyncio.get_event_loop()

logger.info('Loading books list...')

page_content = loop.run_until_complete(get_multiple_pages(loop, 'https://books.toscrape.com/'))
page = BooksPage(page_content[0])
books = page.books

logger.debug('Assigning urls to all pages')
urls = [f'https://books.toscrape.com/catalogue/page-{i}.html' for i in range(2, page.page_count + 1)]
# this works slow for books to scrape


start = time.time()
logger.debug('Downloading content from all pages')
all_page_content = loop.run_until_complete(get_multiple_pages(loop, *urls))
logger.info(f'Total page request took {time.time() - start}')

logger.debug('Extracting data from saved content')
[books.extend(BooksPage(page_content).books) for page_content in all_page_content]


# the old way with requests
# for i in range(2, page.page_count + 1):
#     page_content = requests.get(f'https://books.toscrape.com/catalogue/page-{i}.html').content
#     logger.debug('Extracting data from page content')
#     page = BooksPage(page_content)
#     books.extend(page.books)


