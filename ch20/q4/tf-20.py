import sys, configparser, importlib.machinery

def load_plugins():
    config = configparser.ConfigParser()
    config.read("config.ini")
    words_plugin = config.get("Plugins", "words")
    frequencies_plugin = config.get("Plugins", "frequencies")
    print_plugin = config.get("Plugins", "print")
    global tfwords, tffreqs, tfprint
    tfwords = importlib.machinery.SourcelessFileLoader("tfwords", words_plugin).load_module()
    tffreqs = importlib.machinery.SourcelessFileLoader("tffreqs", frequencies_plugin).load_module()
    tfprint = importlib.machinery.SourcelessFileLoader("tfprint", print_plugin).load_module()

load_plugins()
word_freqs = tffreqs.top25(tfwords.extract_words(sys.argv[1]))
tfprint.pprint(word_freqs)
