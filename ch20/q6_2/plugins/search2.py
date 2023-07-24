def search(words):
    with open('../../target_words.txt') as f:
        target_words = sorted(f.read().split(','))

    results = []
    for target_word in target_words:
        for i, (page, word) in enumerate(words):
            if target_word == word:
                results.append((page, *(words[i+j][1] for j in range(-2, 3))))
    return results

