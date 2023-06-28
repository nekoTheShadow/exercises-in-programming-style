import sys, re


a=[(i//45+1, w)  for i, v in enumerate(open(sys.argv[1])) for w in re.findall("[\w]+", v.lower())]
for t in open('../target_words.txt').read().split(','):
    for i in range(len(a)):
        if a[i][1]==t:
            print(a[i][1],a[i-1][1],a[i][1],a[i+1][1],a[i+2][1],'-',a[i][0])