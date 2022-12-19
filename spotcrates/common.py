from itertools import islice


def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    it = iter(iterable)
    while True:
        batch = list(islice(it, n))
        if not batch:
            return
        yield batch


def get_all_items(spotify, first_page):
    "Collects the 'items' contents from every page in the given result set."
    all_items = []

    all_items.extend(first_page['items'])

    next_page = spotify.next(first_page)
    while next_page:
        all_items.extend(next_page['items'])
        next_page = spotify.next(next_page)

    return all_items