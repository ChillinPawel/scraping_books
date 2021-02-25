import logging


from app import books

logger = logging.getLogger('scraping.menu')

USER_CHOICE = '''Enter one of the following

- 'b' to look at 5-star books
- 'c' to look at the cheapest books
- 'n' to just get the next available book in the catalogue
- 'q' to exit

Enter your choice: '''


books_generator = (book for book in books)


def print_best_books(count=5):
    logger.info('Finding best books...')
    best_books = sorted(books, key=lambda x: (x.rating * -1, x.price))[:count]
    print(f'\nBEST {count} BOOKS:')
    for book in best_books:
        print(book)
    print('\n')


def print_cheapest_books(count=5):
    logger.info('Finding cheapest books...')
    cheapest_books = sorted(books, key=lambda x: x.price)[:count]
    print(f'\nCHEAPEST {count} BOOKS:')
    for book in cheapest_books:
        print(book)
    print('\n')


def print_next_book():
    logger.info('Getting next book from books_generator')
    print(f'\nCURRENT BOOK:\n{next(books_generator)}\n')


def exit_menu():
    print('Exiting... GoodBye')


user_actions = {
    'b': print_best_books,
    'c': print_cheapest_books,
    'n': print_next_book,
    'q': exit_menu
}


def start_menu():
    logger.debug('Starting the menu')
    print(f'<<<--- CUSTOM BOOK SCRAPER --->>>\n')
    user_input = ''  # just for initiation
    while user_input != 'q':
        logger.debug('Getting user input')
        user_input = input(USER_CHOICE)
        if user_input in user_actions:
            user_actions.get(user_input)()
        else:
            print('\nInvalid command!\n')
    logger.debug('Terminating program')


start_menu()
