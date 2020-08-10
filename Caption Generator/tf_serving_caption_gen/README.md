# [Tensorflow-Serving Caption Generator](https://hub.docker.com/r/adityajn105/tf_serving_caption_gen)

A tensorflow/serving api to serve Caption-Generator deep learning model with gRPC and REST interface. 

Model is based on merge-architecture which uses VGG19 to get image embedding and LSTM to generate next word.

## Usage
You can run following commands to get the server running.

	docker image pull adityajn105/tf_serving_caption_gen:latest
		
	docker container run -d -p 8500:8500 -p 8501:8501 --network=bridge --network-alias=tf_server adityajn105/tf_serving_caption_gen:latest

Consume REST api on 8501 port and gRPC on 8500 port.

## Contributors
* [Aditya Jain](https://adityajain.me)