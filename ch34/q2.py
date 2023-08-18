import re, string, sys

with open("../stop_words.txt") as f:
    stops = set(f.read().split(",")+list(string.ascii_lowercase))
data = {}

def error_state():
    return "Something wrong", ["get", "default", None]

def default_get_handler(args):
    rep  = "What would you like to do?\n"
    rep += "1 - Quit\n"
    rep += "2 - Upload file (ASC)\n"
    rep += "3 - Upload file (DESC)"
    links = {
        "1" : ["post", "execution", None], 
        "2" : ["get", "file_form", ["ASC"]],
        "3" : ["get", "file_form", ["DSC"]],
    }
    return rep, links

def quit_handler(args):
    sys.exit("Goodbye cruel world...")

def upload_get_handler(args):
    return "Name of file to upload?", ["post", "file", args]

def upload_post_handler(args):
    def create_data(fn, reverse):
        word_freqs = {}
        with open(fn) as f:
            for w in [x.lower() for x in re.split("[^a-zA-Z]+", f.read()) if len(x) > 0 and x.lower() not in stops]:
                word_freqs[w] = word_freqs.get(w, 0) + 1
        wf = list(word_freqs.items())
        data[fn] = sorted(wf,key=lambda x: x[1],reverse=reverse)

    if args == None:
        return error_state()
    order = args[0]
    filename = args[1]
    try:
        create_data(filename, order=="DSC")
    except:
        print(f"Unexpected error: {sys.exc_info()[0]}")
        return error_state()
    return word_get_handler([filename, 0])

def word_get_handler(args):
    def get_word(filename, word_index):
        if word_index < len(data[filename]):
            return data[filename][word_index]
        else:
            return ("no more words", 0)

    filename = args[0]
    word_index = args[1]
    word_info = get_word(filename, word_index)
    rep  = "\n#{0}: {1} - {2}\n\n".format(word_index+1, word_info[0], word_info[1])
    rep += "What would you like to do next?\n"
    rep += "1 - Quit\n"
    rep += "2 - Upload file (ASC)\n"
    rep += "3 - Upload file (DESC)\n"
    rep += "4 - See next most-frequently occurring word\n"
    links = {"1" : ["post", "execution", None],
             "2" : ["get", "file_form", ["ASC"]],
             "3" : ["get", "file_form", ["DSC"]],
             "4" : ["get", "word", [filename, word_index+1]]}
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
            if len(links) == 2:
                links.append([input])
            else:
                links[2].append(input)
            return links
        else:
            return links
    else:
        return ["get", "default", None]

request = ["get", "default", None]
while True:
    state_representation, links = handle_request(*request)
    request = render_and_get_input(state_representation, links)