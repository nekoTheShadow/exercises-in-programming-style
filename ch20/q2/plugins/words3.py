def extract_words(path_to_file):
    words = []
    with open(path_to_file) as f:
        for line in f:
           words.extend(split(line))
    
    with open('../../stop_words.txt') as f:
        stop_words = split(f.read())

    filtered_words = []
    for word in words:
        if len(word) > 1 and word not in stop_words:
            filtered_words.append(word)
    return filtered_words


def split(line):
    words = []
    chars = []
    for ch in line:
        if ch.isalnum():
            chars.append(ch)
        else:
            if len(chars) > 0:
                words.append(''.join(chars).lower())
                chars.clear()
    if len(chars) > 0:
        words.append(''.join(chars).lower())
    return words
