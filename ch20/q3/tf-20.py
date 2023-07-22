import sys, importlib.machinery

words_suffix = input("[1]words1.pyc [2]words2.pyc : ")
freqs_suffix = input("[1]frequencies1.pyc [2]frequencies2.pyc : ")

tfwords = importlib.machinery.SourcelessFileLoader("tfwords", f"plugins/words{words_suffix}.pyc").load_module()
tffreqs = importlib.machinery.SourcelessFileLoader("tffreqs", f"plugins/frequencies{freqs_suffix}.pyc").load_module()
word_freqs = tffreqs.top25(tfwords.extract_words(sys.argv[1]))

for (w, c) in word_freqs:
    print(w, "-", c)
