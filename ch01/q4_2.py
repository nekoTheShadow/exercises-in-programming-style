import sys, os, shutil

data = [None]*1025

data[0] = open(sys.argv[1])
data[1] = None # 読み込んだ行を保持する
data[2] = None # start index
data[3] = None # current
data[4] = 0 # line number
data[5] = None # word
data[6] = open('q4_2_tmp_words', 'w')

while True:
    data[1] = data[0].readline()
    if data[1] == '':
        break
    
    data[3] = 0
    while True:
        if len(data[1]) <= data[3]:
            break

        if data[2] == None:
            if data[1][data[3]].isalnum():
                data[2] = data[3]
        else:
            if not data[1][data[3]].isalnum():
                data[5] = data[1][data[2]:data[3]].lower()
                data[6].write(data[5] + "," + str(data[4]//45+1) + "\n")
                data[2] = None
        data[3] += 1
    data[4] += 1

data[0].close()
data[6].close()


data[0] = open('../target_words.txt')
data[1] = data[0].readline() 
data[2] = 0 # start_index
data[3] = 0 # current_index
data[4] = open('q4_2_tmp_targets', 'w')

while True:
    if len(data[1]) == data[3]:
        data[4].write(data[1][data[2]:data[3]] + "\n")
        break

    if data[1][data[3]] == ',':
        data[4].write(data[1][data[2]:data[3]] + "\n")
        data[2] = data[3]+1
    data[3] += 1

data[0].close()
data[4].close()


data[0] = None # file pointer
data[1] = "" # last 
data[2] = None # current min
data[3] = None # current line (target)

data[4] = None # file pointer (word)
data[5] = "\n" # line (word)
data[6] = "\n" # line (word)
data[7] = "\n" # line (word)
data[8] = "\n" # line (word)
data[9] = "\n" # line (word)

while True:
    data[0] = open('q4_2_tmp_targets')
    while True:
        data[3] = data[0].readline().strip()
        if data[3] == "":
            break
        if data[1] < data[3] and (data[2] is None or data[3] < data[2]):
            data[2] = data[3]
    data[0].close()

    if data[2] is None:
        break
    
    data[4] = open('q4_2_tmp_words')
    data[5] = "\n" # line (word)
    data[6] = "\n" # line (word)
    data[7] = "\n" # line (word)
    data[8] = "\n" # line (word)
    data[9] = "\n" # line (word)
    while True:
        data[5], data[6], data[7], data[8] = data[6], data[7], data[8], data[9]
        data[9] = data[4].readline()
        if data[5] == "":
            break
        if data[7].split(",")[0] == data[2]:
            print(data[5].split(",")[0].strip(),
                  data[6].split(",")[0].strip(),
                  data[7].split(",")[0].strip(),
                  data[8].split(",")[0].strip(),
                  data[9].split(",")[0].strip(),
                  '-', 
                  data[7].split(",")[1].strip())

    data[4].close()
    
    data[1] = data[2]
    data[2] = None
    
    
