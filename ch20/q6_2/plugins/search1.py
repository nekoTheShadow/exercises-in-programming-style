def search(words):
    with open('../../target_words.txt') as f:
        target_words = f.read().split(',')
    target_words.sort()

    results = []
    for target_word in target_words:
        for i, (page, word) in enumerate(words):
            if target_word == word:
                results.append((page, words[i-2][1], words[i-1][1], words[i][1], words[i+1][1], words[i+2][1]))
    return results

