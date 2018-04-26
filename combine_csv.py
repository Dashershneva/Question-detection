import os
import numpy
import csv
import json

import kaldi

csv_path = os.listdir(path='result')
align = 'new_alignments.json'
features_dict = dict()

with open(align, encoding='utf-8') as json_file:
    for line in json_file:
        line = json.loads(line)
        path_list = []
        for path in csv_path:
            if path.startswith("%s-" %(str(line["ID"]))):
                path_list.append(path)
        print(path_list)
        ar = numpy.array([]).reshape((0, 349))
        for p in path_list:
            with open('result/' + p, encoding='utf-8', newline='') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    if row != [] and row[0].startswith("'noname"):
                        row.remove("'noname'")
                        row.remove('unknown')
                        i = 0
                        while i < len(row):
                            row[i] = float(row[i])
                            i += 1
                        b = numpy.array([row])
                        ar = numpy.concatenate((ar, b), axis=0)
                        # print(row)
        print(line['ID'], "array:", numpy.shape(ar.transpose()))
        bt = bytes(str(line['ID']), 'utf-8')
        features_dict[bt] = ar.transpose()
        #print(type(features_dict[bt]))

print(len(features_dict))


with open("output.ark", "wb") as fp:
    kaldi.dumpark(features_dict, fp)


"""
ar = numpy.array([]).reshape((0,3))
print(ar)
b = numpy.array([[1,2,3]])
ar = numpy.concatenate((ar, b), axis=0)
print(ar)
print(ar.transpose())
"""