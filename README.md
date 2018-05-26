# Question-detection

Model for question detection is in model_question_detection.ipynb

Data files for model reatning and testing are in data_ord folder.

alignments.json contains words alignments for phrases.
index.json contains transcriptions of all phrases.

Acoustic and lexical features are in feat.ark and embeddings.ark

To run the model you need to have module tensorflow version 1.2 or higher.
There ate three types of models: acoustic, lexical or hybrid. To choose the model select one of the following modes:

MODE = MODE_ACOUSTIC
MODE = MODE_TEXT
MODE = MODE_HYBRID

Firstly, model processes the input data and parses it into named tuples. At this point model excludes sentences with mistakes in alignments and sentences longer than 30 words.

Futher parsed data goes to tf.Graph() module where it's fed to lstm.

Train question prediction block shows the process of learning on train, validation and test sets.
There are scores for each epoch of learning. Learning stops when the AUC scores stops increasing.

The model shows accuracy of 86% and AUC 85% for hybrid model.

To plot the results use test_roc(graph, data_test, model="purpose") function.
