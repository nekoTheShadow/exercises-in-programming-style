def group_by(words):
    pages = {}
    for page, word in words:
        if word not in pages:
            pages[word] = []
        if page not in pages[word]:
            pages[word].append(page)
    return pages