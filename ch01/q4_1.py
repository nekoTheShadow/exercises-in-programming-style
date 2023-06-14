import sys, os, shutil

# 事前準備
shutil.rmtree('q4_1_tmp')
os.mkdir('q4_1_tmp')

data = [None]*1025
data[0] = open(sys.argv[1])
data[1] = None # 読み込んだ行を保持する
data[2] = None # start index
data[3] = None # current
data[4] = 0 # line number
data[5] = None # word
data[6] = None # pointer

while True:
    data[1] = data[0].readline()
    if data[1] == '':
        break
    
    data[3] = 0
    while True:
        if len(data[1]) <= data[3]:
            break

        if data[2] == None:
            if data[1][data[3]].isalpha():
                data[2] = data[3]
        else:
            if not data[1][data[3]].isalpha():
                data[5] = data[1][data[2]:data[3]].lower()
                if not os.path.exists('q4_1_tmp' + '/' + data[5]):
                    data[6] = open('q4_1_tmp/all_words', 'a')
                    data[6].write(data[5] + "\n")
                    data[6].close()
                data[6] = open('q4_1_tmp' + '/' + data[5], 'a')
                data[6].write(str(data[4]//45+1) + "\n")
                data[6].close()

                data[2] = None
        data[3] += 1
    
    data[4] += 1

data[0].close()

data[0] = None
data[1] = "" # current
data[2] = "" # last
data[3] = None # current min

data[4] = None # fp
data[5] = None # current line
data[6] = None # last page
data[7] = None # formatted line
data[8] = 0    # counter

while True: 
    data[0] = open('q4_1_tmp/all_words')
    data[3] = None
    while True:
        data[1] = data[0].readline()
        if data[1] == "":
            break
        data[1] = data[1].strip()
        if data[2] < data[1] and (data[3] is None or data[1] < data[3]):
            data[3] = data[1]
    
    data[0].close()
    if data[3] is None:
        break

    data[4] = open('q4_1_tmp/' + data[3])
    data[6] = ""
    data[7] = data[3] + " - "
    data[8] = 0
    while True:
        data[5] = data[4].readline()
        if data[5] == "":
            break
        if data[6] != data[5]:
            if data[8] != 0:
                data[7] += ", "
            data[7] += data[5].strip()
            data[6] = data[5]
            data[8] += 1
    data[4].close()
    if data[8] < 100:
        print(data[7])

    data[2] = data[3] 
    

