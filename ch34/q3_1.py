import re, string, sys, collections

with open("../stop_words.txt") as f:
    stops = set(f.read().split(",")+list(string.ascii_lowercase))
data = {}

def error_state():
    return "Something wrong", ["get", "default", None]

def default_get_handler(args):
    rep  = "What would you like to do?\n"
    rep += "1 - Quit\n"
    rep += "2 - Upload file"
    links = {
        "1" : ["post", "execution", None], 
        "2" : ["get", "file_form", ["ASC"]],
    }
    return rep, links

def quit_handler(args):
    sys.exit("Goodbye cruel world...")

def upload_get_handler(args):
    return "Name of file to upload?", ["post", "file"]

def upload_post_handler(args):
    def create_data(fn):
        word_freqs = collections.defaultdict(set)
        with open(fn) as f:
            for i, line in enumerate(f):
                for w in re.findall("[a-z]+", line.lower()):
                    word_freqs[w].add(i//45+1)
        data[fn] = sorted((w, list(sorted(page))) for w, page in word_freqs.items() if len(page) < 100)

    if args == None:
        return error_state()
    filename = args[0]
    try:
        create_data(filename)
    except:
        print(f"Unexpected error: {sys.exc_info()[0]}")
        return error_state()
    return word_get_handler([filename, 0])

def word_get_handler(args):
    filename = args[0]
    word_index = args[1]
    if word_index < len(data[filename]):
        word_info = data[filename][word_index]
        rep = "\n#{0}: {1} - {2}\n\n".format(word_index+1, word_info[0], ', '.join(map(str, word_info[1])))
    else:
        rep = "\n no more words \n\n"
    rep += "What would you like to do next?\n"
    rep += "1 - Quit\n"
    rep += "2 - Upload file\n"
    rep += "3 - See next word\n"
    links = {"1" : ["post", "execution", None],
             "2" : ["get", "file_form"],
             "3" : ["get", "word", [filename, word_index+1]]}
    return rep, links

handlers = {"post_execution" : quit_handler,
            "get_default" : default_get_handler,
            "get_file_form" : upload_get_handler,
            "post_file" : upload_post_handler,
            "get_word" : word_get_handler }

def handle_request(verb, uri, args):
    def handler_key(verb, uri):
        return verb + "_" + uri
    if handler_key(verb, uri) in handlers:
        return handlers[handler_key(verb, uri)](args)
    else:
        return handlers[handler_key("get", "default")](args)

def render_and_get_input(state_representation, links):
    print(state_representation)
    sys.stdout.flush()
    if type(links) is dict:
        input = sys.stdin.readline().strip()
        if input in links:
            return links[input]
        else:
            return ["get", "default", None]
    elif type(links) is list:
        if links[0] == "post":
            input = sys.stdin.readline().strip()
            links.append([input])
            return links
        else:
            return links
    else:
        return ["get", "default", None]

request = ["get", "default", None]
while True:
    state_representation, links = handle_request(*request)
    request = render_and_get_input(state_representation, links)