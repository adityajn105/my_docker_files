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
nertag = load_model('saved_items/ner_tagging_model.h5')
tokens = pkl.load( open('saved_items/tokens.pkl','rb') )

ner_dict = {0: 'O', 1: 'B-geo', 2: 'B-gpe', 3: 'B-per', 4: 'I-geo', 5: 'B-org', 6: 'I-org', 7: 'B-tim', 8: 'B-art',
 9: 'I-art', 10: 'I-per', 11: 'I-gpe', 12: 'I-tim', 13: 'B-nat', 14: 'B-eve', 15: 'I-eve', 16: 'I-nat'}

def getTagsSentence( words ):
    inp_seq = []
    for word in words:
        inp_seq.append( tokens.get( word.lower(), UNK_IDX ) )
    ln = len(inp_seq)
    inp_seq += [0]*(MAX_SEQ_LEN-ln)
    inp_embeddings = embedding.predict( np.expand_dims(inp_seq, axis=0) )
    out_seq = nertag.predict( inp_embeddings )[0]
    tags = [ ner_dict[np.argmax(pos)] for pos in out_seq ][:ln]
    return list(zip( words, tags ))

def getNerWhole( para ):
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