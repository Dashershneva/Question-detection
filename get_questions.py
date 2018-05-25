import wave
from pydub import AudioSegment
import os
import csv
import re

transcripts = os.listdir(path="transcripts")
audios = os.listdir(path="audio")

file_names = []
with open('C:/Users/dsher/PycharmProjects/speech_recognition/sentences_subtitles.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for row in reader:
        file_names.append(row['path'])

with open('questions_subtitles_updated.csv', 'a', encoding='utf-8', newline='') as new_csvfile:
    fieldnames = ['path', 'transcript', 't1', 't2', 'quest_num']
    writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()


# get all questions and their durations from subtitles
def  get_questions(subtitle):
    srt = open(subtitle, 'r', encoding="utf-8")
    lines = srt.readlines()
    correct_diration = {}
    i = 0
    for line in lines:
        if '?' in line and lines[i-1].startswith('0'):
            text = line
            dur = lines[i-1]
            dur = dur.replace(':','')
            dur = dur.replace(',','.')
            dur_list = dur.split(' --> ')
            t1 = dur_list[0]
            t2 = dur_list[1]
            if text in correct_diration:
                correct_diration[text]['t2'] = t2
            else:
                correct_diration[text] = {'t1':t1, 't2':t2}
            print(text, dur, t1, t2)
        i+=1
    print(correct_diration)
    return srt

def process_audio(audio):
    audio = wave.open(audio, 'r')
    channel = audio.getnchannels()
    frame = audio.getframerate()
    metrics = (channel, frame)
    audio.close()
    return metrics

# cut questions in .wav from big audiofiles
def sample_questions():
    with open('sentences_subtitles.csv', 'r',
              encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        i = 0
        n = 0
        for row in reader:
            t1 = row['t1']
            t1 = float(t1)*1000
            t1 = int(t1)
            t2 = row['t2']
            t2 = float(t2)*1000
            t2 = int(t2)
            # print(i, row['path'], t1, t2)
            if row['path'] + ".wav" in audios and t1!=t2:
                audio = "audio/" + row['path'] + '.wav'
                neqst = 'questions_wav/%s_sentence_%s.wav' %(row['path'],str(i))
                readAudio= AudioSegment.from_wav(audio)
                newAudio = readAudio[t1:t2]
                print(i, audio, t1, t2, len(readAudio), len(newAudio))
                newQuestion = newAudio.export('questions_wav/%s_sentence_%s.wav' %(row['path'],str(i)), format='wav')
                """
                with open('questions_subtitles_updated.csv', 'a', encoding='utf-8', newline='') as new_csvfile:
                    fieldnames = ['path', 'transcript', 't1', 't2', 'quest_num']
                    writer = csv.DictWriter(new_csvfile, fieldnames=fieldnames, delimiter='\t')
                    writer.writerow({'path': row['path'], 'transcript': row['transcript'],
                                     't1': row['t1'], 't2': row['t2'], 'quest_num': neqst})
                                     """
            i+=1
    return  reader


def main():
    sample_questions()


if __name__ == '__main__':
    main()
