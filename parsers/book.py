import re
import logging

from locators.book_locators import BookLocators

logger = logging.getLogger('scraping.book_parser')


class BookParser:
    """
    Given one of the specific book article, finds out the data about
    the book (title, price, rating, link)
    """

    RATINGS = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    def __init__(self, parent):
        logger.debug(f'New book parser created from `{parent}`.')
        self.parent = parent

    def __repr__(self):
        multiple = 's' if self.rating > 1 else ''
        return f'<{self.title}, £{self.price}, rated {self.rating}/5 star{multiple}>'

    @property
    def title(self):
        logger.debug('Looking for the book title...')
        locator = BookLocators.TITLE_LINK
        title = self.parent.select_one(locator).attrs['title']
        logger.debug(f'Found the book title, `{title}`.')
        return title

    @property
    def link(self):
        logger.debug('Looking for the book link...')
        locator = BookLocators.TITLE_LINK
        link = self.parent.select_one(locator).attrs['href']
        logger.debug(f'Found the book link, `{link}`.')
        return link

    @property
    def price(self):
        logger.debug('Looking for the book price...')
        locator = BookLocators.PRICE
        item_price = self.parent.select_one(locator).string
        pattern = '£(\d+\.\d{2})'
        float_price = float(re.search(pattern, item_price).group(1))
        logger.debug(f'Found the book price, `{float_price}`.')
        return float_price

    @property
    def rating(self):
        logger.debug('Looking for the book rating...')
        locator = BookLocators.RATING
        star_rating_tag = self.parent.select_one(locator)
        rating_class = [cls for cls in star_rating_tag.attrs['class'] if cls != 'star-rating']
        rating_number = BookParser.RATINGS.get(rating_class[0], 0)
        logger.debug(f'Found the book rating, `{rating_number}`')
        return rating_number
