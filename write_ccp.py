import os
import csv
import re
import subprocess

datapath = 'cut_sentences/'

all_audio = os.listdir(datapath)


def write_scp(all_audio):
    i = 1
    ordered_audios = sorted(all_audio, key=lambda x: (int(re.sub('\D', '', x)), x))
    for path in all_audio:
        with open('questions_norm.scp', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            string = str(str(i) + ' sox ' + "cut_sent_norm\\" + str(path) + ' -r 16000 -b 16 -c 1 -t wav - |')
            #string = str(str(i) + ' sox ' + "cut_sent\\" + str(path) + "cut_sent_norm\\" + str(path))
            writer.writerow(string)
            print(string)
        i+=1
    return all_audio

def rewrite_audio():
    with open('questions_normalize.scp', encoding='utf-8') as scpfile:
        for line in scpfile:
            print(line)
            subprocess.call(line.split())


def main():
    write_scp(all_audio)
    #rewrite_audio()

if __name__ == '__main__':
    main()