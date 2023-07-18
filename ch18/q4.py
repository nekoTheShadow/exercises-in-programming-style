import sys
with open(sys.argv[2]) as f:
    exec(f.read())
run(sys.argv[1])

# python3 q4.py ../pride-and-prejudice.txt q4_1.txt
# python3 q4.py ../pride-and-prejudice.txt q4_2.txt