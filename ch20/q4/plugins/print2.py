def pprint(word_freqs):
    print('\n'.join(f'{w} - {c}' for w, c in word_freqs))