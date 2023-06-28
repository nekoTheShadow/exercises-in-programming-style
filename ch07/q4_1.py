import sys, re, collections
s=open('../stop_words.txt').read().split(',')

d=collections.defaultdict(list)
for i, v in enumerate(open(sys.argv[1])):
    for w in re.findall("[a-z]{2,}", v.lower()):
        if w not in s:
            d[w].append(i//45+1)

for k in sorted(d):
    if len(d[k])<100:
        print(k, '-', ', '.join(map(str, d[k])))