# [Digit Recognizer App](https://hub.docker.com/r/adityajn105/digit_recognizer_app)

A web app to recognizer drawn digits on HTML5 canvas.

It uses Convolution Neural Network trained on MNIST dataset to classify digits.

## Usage
You can run following commands to get the app running.

	docker pull adityajn105/digit_recognizer_app:latest
		
	docker run -d -p 80:80 -v stats:/home/app/stats adityajn105/digit_recognizer_app:latest

Get app in your browser by visiting `http://localhost`.

## Contributors
* [Aditya Jain](https://adityajain.me)