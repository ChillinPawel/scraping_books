import re
import logging

from bs4 import BeautifulSoup

from locators.books_page_locators import BooksPageLocators
from parsers.book import BookParser

logger = logging.getLogger('scraping.all_books_page')


class BooksPage:
    def __init__(self, page):
        logger.debug('Parsing page content with BeautifulSoup HTML parser.')
        self.soup = BeautifulSoup(page, 'html.parser')

    @property
    def books(self):
        logger.debug(f'Locating books in the page using `{BooksPageLocators.BOOK}`.')
        return [BookParser(e) for e in self.soup.select(BooksPageLocators.BOOK)]

    @property
    def page_count(self):
        logger.debug('Locating all number of catalogue pages available')
        page = self.soup.select_one(BooksPageLocators.PAGE_NUMBER).string
        logger.info(f'Found number of catalogue pages available: `{page}`.')
        pattern = 'Page \d+ of (\d+)'
        pages = int(re.search(pattern, page).group(1))
        logger.debug(f'Extracted number of pages as integer: `{pages}`.')
        return pages

