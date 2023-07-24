def pprint(pages):
    print('\n'.join("%s - %s" % (e[0], ', '.join(map(str, e[1]))) for e in sorted(pages.items(), key=lambda e : e[0]) if len(e[1]) < 100))