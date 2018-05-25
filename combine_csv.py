import os
import numpy
import csv
import json
from collections import defaultdict

import kaldi

csv_path = os.listdir(path=r'result/result')
align = 'alignments.json'
features_dict = dict()

def remove_empty():
    for path in csv_path:
        with open('result//result//' + path, encoding='utf-8', newline='') as csv_file:
            reader = csv.reader(csv_file)
            rows = []
            for row in reader:
                rows.append(row)
            csv_file.close()
            # print(path, rows[-1])
        if rows[-1] == []:
            os.remove('result//result//' + path)
            print(path, ' removed')



def csv_to_ark():
    word_features = defaultdict(list)
    for path in csv_path:
        tokens = path.replace(".", "-").split("-")
        #print(tokens)
        utterance = tokens[0]
        word_id = int(tokens[2])
        word_features[utterance].append((word_id, path))
    with open(align, encoding='utf-8') as json_file:
        for line in json_file:
            line = json.loads(line)
            path_list = [record[1] for record in
                         sorted(word_features[str(line["ID"])], key=lambda r: r[0])]
            ar = numpy.array([]).reshape((0, 349))
            for p in path_list:
                with open(r'result/result/' + p, encoding='utf-8', newline='') as csv_file:
                    lines = csv_file.readlines()
                    #print(len(lines))
                    #print(lines[-1])
                    row = lines[-1].strip().split(",")
                    if row != [] and row[0].startswith("'noname"):
                        row.remove("'noname'")
                        row.remove('unknown')
                        print(len(row))
                        i = 0
                        while i < len(row):
                            row[i] = float(row[i])
                            i += 1
                        b = numpy.array([row])
                        ar = numpy.concatenate((ar, b), axis=0)
                        # print(row)
            #print(line['ID'], "array:", numpy.shape(ar.transpose()))
            bt = bytes(str(line['ID']), 'utf-8')
            if path_list != []:
                features_dict[bt] = ar.transpose()
            #print(type(features_dict[bt]))

    print(len(features_dict))
    print(features_dict[b"3"].shape)

    with open("feat_norm.ark", "wb") as fp:
        kaldi.dumpark(features_dict, fp)

def main():
    #remove_empty()
    csv_to_ark()

if __name__ == '__main__':
    main()