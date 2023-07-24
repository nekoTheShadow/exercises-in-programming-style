import collections

def group_by(words):
    pages = collections.defaultdict(list)
    for page, word in words:
        if page not in pages[word]:
            pages[word].append(page)
    return pages