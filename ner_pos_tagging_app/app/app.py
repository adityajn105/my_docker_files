from flask import Flask, render_template, request, jsonify, redirect
from postagging import getPosWhole
from nertagging import getNerWhole

import os
app = Flask(__name__)

pos_color = {
    '<pad>': ('padding', '#d2cac9'),
    '.': ('sentence end', '#826148' ),
     '``': ('quotes', '#ccd5ff'),
     ',': ('sentence/item seperation','#ffb947' ),
     ':': ('colon', '#c0cbff'),
     ';': ('semicolon','#ff66ff' ),
     '$': ('$','#00ffcc' ),
    'CC': ('coordinating conjunction','#f2f2bc' ),
    'CD': ('cardinal digit', '#c1c196'),
    'DT': ('determiner', '#d1876d'),
    'EX': (' existential there (like: “there is” … think of it like “there exists”)', '#00a3cc'),
    'FW': ('foregin word', '#f1c0af'),
    'IN': ('preposition/subordinating conjunction','#1488c5' ),
    'JJ' : ('adjective, or numeral, ordinal','#7ac5cd' ),
    'JJR': ('adjective, comparative', '#619da4'),
    'JJS': ('adjective, superlative', '#a1d6dc'),
    'LS': ('list item marker','#f2f2bc' ),
    'LRB': ('Braces', '#a9a983'),
    'MD' : ('modal auxiliary', '#f4f4c9'),
    'NN': ('noun, common, singular', '#ff7256'), 
    'NNP' : ( 'noun, proper, singular',  '#ff8066'), 
    'NNS' : ('noun, common, plural','#ff8e77' ),
    'NNPS': ('proper noun, plural ‘Americans’', '#ff9c88'),
    'PDT' : ('pre-determiner','#e9967a' ), 
    'POS' : ('possessive ending parent’s', '#eba087'),
    'PRP': ('pronoun, personal','#a9a9d9' ),
    'PRP$': ('pronoun, possessive','#8787ad' ),
    'RB': ('adverb', '#7ac5cd'), 
    'RBR' : ('adverb, comparative', '#619da4'),
    'RBS' : ('adverb, superlative','#94d0d7' ),
    'RP': ('particle give up','#afdce1' ),
    'TO': ('to go ‘to’ the store.', '#ddc4c4'),
    'UH': ('interjection errrrrrrrm', '#b09c9c'),
    'VB': ('verb, base form', '#87ae7c'),
    'VBD' : ('verb, past tense', '#9fbe96'),
    'VBG' : ('verb, present participle','#5e7956' ),
    'VBN' : ('verb, past participle','#799c6f' ),
    'VBP' : ('verb, not 3rd person','#b7ceb0' ),
    'VBZ': ('verb, 3rd person', '#c3d6bd'),
    'WDT': ('WH-determiner', '#c2a292'),
    'WP': ('WH-pronoun','#dac7bd' ),
    'WP$':('WP$ possessive wh-pronoun whose','#9b8174' ),
    'WRB': ('Wh-adverb','#ceb4a7' )
}

ner_color = { 'O' : ( "na", '#ededfb'),
    'B-geo' : ( 'Geographic entity beginning Token', '#6c8b63' ),
    'I-geo' : ( 'Geographic entity inside Token', '#87ae7c' ),
    'B-gpe' : ( 'Geo-political entity beginning Token', '#d8b680' ),
    'I-gpe' : ( 'Geo-political entity inside Token', '#f0cb8f' ),
    'B-per' : ( 'Person Name entity beginning Token', '#1488c5' ),
    'I-per' : ( 'Person Name entity inside Token', '#429fd0' ),
    'B-org' : ( 'Organization entity beginning Token', '#e5664d' ),
    'I-org' : ( 'Organization entity inside Token', '#ff7256' ),
    'B-art' : ( 'Art entity beginning Toekn', '#d1876d' ),
    'I-art' : ( 'Art entity inside Token', '#e9967a' ),
    'B-tim' : ( 'Time entity beginning Token', '#888888' ),
    'I-tim' : ( 'Time entity inside Token', '#aaaaaa' ),
    'B-nat' : ( '', '#ab4cab' ),
    'I-nat' : ( '', '#c37fc3' ),
    'I-eve' : ( 'Event entity inside Token', '#c8ab9c' ),
    'B-eve' : ( 'Event entity beginning Token', '#ae9183')
}


@app.route('/', methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        sentences = request.form.get('sentence').strip()
        typ = request.form.get('type')
        if typ=='pos':
            tags = getPosWhole(sentences)
            tags = [ ( word, tag, *pos_color[tag] ) for word, tag in tags ]
            return render_template('index.html', data = {'status':True, 'tags':tags, 'text':sentences })
        elif typ=='ner':
            tags = getNerWhole(sentences)
            tags = [ ( word, tag, *ner_color[tag] ) for word, tag in tags ]
            return render_template('index.html', data = {'status':True, 'tags':tags, 'text':sentences })
        else:
            return render_template('index.html', data = {'status':False, 'text':""})
    elif request.method == 'GET':
        sentences = request.args.get('sentence')
        typ = request.args.get('type')
        if typ==None and sentences==None:
             return render_template('index.html', data = {'status':False, 'text':""})
        elif typ=='pos' and sentences != None:
            tags = getPosWhole(sentences.strip())
            return jsonify({
                'status': True,
                'message': 'POS tags generated',
                'tags': tags
            }); 
        elif typ=='ner' and sentences != None:
            tags = getNerWhole(sentences.strip())
            return jsonify({
                'status': True,
                'message': 'NER tags generated',
                'tags': tags
            });
        else:
            return jsonify({
                'status': False,
                'message': 'Invalid request',
                'tags': []
            });
    else:
         return render_template('index.html', data = {'status':False, 'text':""})

if __name__=='__main__':
    app.run(host = '0.0.0.0', port = int(80))
    print("Application ready to use")