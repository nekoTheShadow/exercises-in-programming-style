def pprint(results):
    print('\n'.join('%s - %s' % (' '.join(r[1:]), r[0]) for r in results))