import re, string, sys, collections

stops = set(open('../stop_words.txt').read().split(',') + list(string.ascii_lowercase))
# words = [x.lower() for x in re.split('[^a-zA-Z]+', open(sys.argv[1]).read()) if len(x) > 0 and x.lower() not in stops]
# unique_words = list(set(words))
# unique_words.sort(key=lambda x : words.count(x), reverse=True)
words = collections.Counter(x.lower() for x in re.split('[^a-zA-Z]+', open(sys.argv[1]).read()) if len(x) > 0 and x.lower() not in stops)
unique_words = list(words.keys())
unique_words.sort(key=lambda x : words[x], reverse=True)
print("\n".join(["%s - %s" % (x, words[x]) for x in unique_words[:25]]))