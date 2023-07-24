def pprint(pages):
    for word in sorted(pages):
        if len(pages[word]) < 100:
            print(word, '-', ', '.join(map(str, pages[word])))