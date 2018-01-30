import os
import csv

transcripts = os.listdir(path="C:/Users/dsher/PycharmProjects/speech_recognition/transcripts")

with open('questions_subtitles.csv', 'a', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['path', 'transcript', 't1', 't2']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()

def  get_questions(subtitle):
    audio_name = subtitle.replace(".srt","")
    subtitle = "C:/Users/dsher/PycharmProjects/speech_recognition/transcripts/" + subtitle
    srt = open(subtitle, 'r', encoding="utf-8")
    lines = srt.readlines()
    correct_diration = {}
    i = 0
    for line in lines:
        if '?' in line and lines[i-1].startswith('0'):
            text = line
            text = text.rstrip()
            dur = lines[i-1]
            dur = dur.replace('00:', '')
            dur = dur.replace(',', '.')
            sec = dur.split(':')
            dur_list = dur.split(' --> ')
            dur_list[1] = dur_list[1].rstrip()
            print(dur_list)
            if ":" in dur_list[0]:
                time1 = dur_list[0].split(':')
                t1 = float(time1[0])*60+float(time1[1])
                time2 = dur_list[1].split(':')
                t2 = float(time2[0])*60+float(time2[1])
            else:
                t1 = dur_list[0]
                t2 = dur_list[1]
            print(t1, t2)
            if text in correct_diration:
                correct_diration[text]['t2'] = t2
            else:
                correct_diration[text] = {'t1':t1, 't2':t2}
            #print(text, dur, t1, t2)
            #print(correct_diration[text]['t1'], correct_diration[text]['t2'])
        i+=1

    for record in correct_diration:
        with open('questions_subtitles.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
            writer.writerow({'path':audio_name, 'transcript':record,
                         't1':correct_diration[record]['t1'], 't2':correct_diration[record]['t2']})
        #print(subtitle, record, correct_diration[record]['t1'], correct_diration[record]['t2'])
    return srt

def main():
    for subtitle in transcripts:
        get_questions(subtitle)

if __name__ == '__main__':
    main()