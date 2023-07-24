def pprint(results):
    for result in results:
        print(*result[1:], '-', result[0])