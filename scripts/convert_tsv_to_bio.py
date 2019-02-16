

import sys

in_path = sys.argv[1]
out_path = sys.argv[2]

fin = open(in_path)
fout = open(out_path, "w")

for line in fin:
    sentence, tags = line.strip("\n").split("\t")
    tokens = sentence.lower().split()
    tags = tags.split()
    if tokens[0] == 'bos':
        tokens = tokens[1:-1]
        tags = tags[1:-1]
    for token,tag in zip(tokens,tags):
        fout.write(tag + "\t" + token + "\n" )
    fout.write("\n")

fout.close()
fin.close()

