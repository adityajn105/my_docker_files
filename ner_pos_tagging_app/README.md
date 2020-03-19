# [NER/POS tagging app](https://hub.docker.com/r/adityajn105/ner_pos_tagging_app)

A deep learning based pos/ner tagging web application provides web interface as well as ReST-Api calls to get your tags. 

It uses LSTM and glove embeddings to find best tags.

## Usage
You can run following commands to get the app running.

	docker pull adityajn105/ner_pos_tagging_app:latest
		
	docker run -d -p 80:80 adityajn105/ner_pos_tagging_app:latest

Get app in your browser by visiting `http://localhost`.


*Alternatively you can use app as ReST Api*

* For Named entity recognition use.

        curl -X GET "http://localhost?sentence=This+application+is+made+by+Aditya.&type=ner"

* For Part of Speech Tagging use:
    
        curl -X GET "http://localhost?sentence=This+application+is+made+by+Aditya.&type=pos"

* It will return a json output as,
    ```
    {
        'status': True,
        'message': 'Description of response generated',
        'tags' : list of tags 
    }
    ```

## Contributors
* [Aditya Jain](https://adityajain.me)