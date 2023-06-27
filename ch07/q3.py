import re,sys,collections
s=open('../stop_words.txt').read().split(',')
for k,v in collections.Counter([w for w in re.findall("[a-z]{2,}",(open(sys.argv[1]).read().lower())) if w not in s]).most_common(25):print(k,'-',v)