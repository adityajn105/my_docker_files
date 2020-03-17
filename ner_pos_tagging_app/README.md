# [NER/POS tagging app](https://hub.docker.com/r/adityajn105/ner_pos_tagging_app)

A deep learning based pos/ner tagging web application provides web interface as well as ReST-Api calls to get your tags. 

It uses LSTM and glove embeddings to find best tags.

## Usage
You can run following commands to get the app running.

	docker pull adityajn105/ner_pos_tagging_app:20.3.18
		
	docker run -d -p 80:80 adityajn105/ner_pos_tagging_app:20.3.18

Get app in your browser by visiting `http://localhost`.

## Contributors
* [Aditya Jain](https://adityajain.me)