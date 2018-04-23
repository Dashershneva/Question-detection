import os
import csv

all_audio = os.listdir('C:/Users/dsher/PycharmProjects/speech_recognition/cut_sent')


def write_scp(all_audio):
    i = 1
    for path in all_audio:
        with open('cut_questions.scp', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            string = str(str(i) + ' sox ' + "cut_sent\\" + str(path) + ' -r 16000 -b 16 -c 1 -t wav - |')
            writer.writerow(string)
            print(string)
        i+=1
    return all_audio

def main():
    write_scp(all_audio)

if __name__ == '__main__':
    main()