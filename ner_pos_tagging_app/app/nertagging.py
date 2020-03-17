from tensorflow.keras.models import load_model
import pickle as pkl
import numpy as np

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


def getTagsSentence( sentence ):
    inp_seq = []
    words = sentence.split()
    for word in words:
        inp_seq.append( tokens.get( word.lower(), UNK_IDX ) )
    ln = len(inp_seq)
    inp_seq += [0]*(MAX_SEQ_LEN-ln)
    inp_embeddings = embedding.predict( np.expand_dims(inp_seq, axis=0) )
    out_seq = nertag.predict( inp_embeddings )[0]
    tags = [ ner_dict[np.argmax(pos)] for pos in out_seq ][:ln]
    return list(zip( words, tags ))

def getNerWhole( para ):
    sentences = []
    sent = []
    for c in list(para):
        if c in [';', '(', ')' ]: 
            sent.append( f' {c} ' )
        elif c in ['!','.','?', ',']:
            sent.append( f' {c}' )
            sentences.append( ("".join(sent)).strip() )
            sent=[]
        else:
            sent.append(c)
    if len(sent)>0: sentences.append(("".join(sent)).strip())
    tags = []
    for sentence in sentences:
        sent_tags = getTagsSentence(sentence) 
        tags.extend( sent_tags )
    return tags