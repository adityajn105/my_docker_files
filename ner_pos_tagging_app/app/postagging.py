from tensorflow.keras.models import load_model
import pickle as pkl
import numpy as np
import re

MAX_SEQ_LEN = 40
VOCAB_SIZE = 400001
EMBEDDING_DIM = 50
POS_SIZE = 43
UNK_IDX = 201535

embedding = load_model('saved_items/embedding_model.h5' )
postag = load_model('saved_items/pos_tagging_model.h5')
tokens = pkl.load( open('saved_items/tokens.pkl','rb') )

pos_dict = { 0: '<pad>', 1: 'NNS', 2: 'IN', 3: 'VBP', 4: 'VBN', 5: 'NNP', 6: 'TO', 7: 'VB', 8: 'DT', 9: 'NN', 10: 'CC', 11: 'JJ', 12: '.', 13: 'VBD', 14: 'WP', 15: '``', 16: 'CD',
17: 'PRP', 18: 'VBZ', 19: 'POS', 20: 'VBG', 21: 'RB', 22: ',', 23: 'WRB', 24: 'PRP$', 25: 'MD', 26: 'WDT', 27: 'JJR', 28: ':', 29: 'JJS', 30: 'WP$', 31: 'RP', 32: 'PDT', 33: 'NNPS',
34: 'EX', 35: 'RBS', 36: 'LRB', 37: 'RRB', 38: '$', 39: 'RBR', 40: ';', 41: 'UH', 42: 'FW'}


def getTagsSentence( words ):
    inp_seq = []
    for word in words:
        inp_seq.append( tokens.get( word.lower(), UNK_IDX ) )
    ln = len(inp_seq)
    inp_seq += [0]*(MAX_SEQ_LEN-ln)
    inp_embeddings = embedding.predict( np.expand_dims(inp_seq, axis=0) )
    out_seq = postag.predict( inp_embeddings )[0]
    tags = [ pos_dict[np.argmax(pos)] for pos in out_seq ][:ln]
    return list(zip( words, tags ))

def getPosWhole( para ):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', para)
    tags = []
    for sentence in sentences:
        sentence = re.sub( "'s|’s", " 's", sentence.strip())
        sentence = re.sub( "s' ", "s ' ", sentence.strip())
        sentence = sentence[:-1]+" "+sentence[-1]
        final = []
        for c in sentence:
            if c in [ '(', ')', ';', ',', '!', ':', '-', '—', '"' ]: final.append( f' {c} ' )
            else: final.append(c)
        sentence = "".join(final).split()
        sent_batches = (len(sentence)//40)+1
        for i in range(sent_batches):
            tags.extend( getTagsSentence(sentence[ i*40: (i+1)*40 ]) )
    return tags