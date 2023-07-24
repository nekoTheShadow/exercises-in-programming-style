import configparser
import importlib
import sys


config = configparser.ConfigParser()
config.read("config.ini")

tfwords = importlib.machinery.SourcelessFileLoader("tfwords", config.get("Plugins", "words")).load_module()
tfgroup = importlib.machinery.SourcelessFileLoader("tffreqs", config.get("Plugins", "group")).load_module()
tfprint = importlib.machinery.SourcelessFileLoader("tfprint", config.get("Plugins", "print")).load_module()

tfprint.pprint(tfgroup.group_by(tfwords.read_words(sys.argv[1])))