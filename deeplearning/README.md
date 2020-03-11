# [Deeplearning Container](https://hub.docker.com/r/adityajn105/deeplearning)

A ready to use container for deeplearning (tensorflow-v2) related project. It is available with vscode and jupyter notebook.

vscode will run on port 5000 and notebook will run on 8888. Another port 3000 is available for user specific purposes.

## Usage
You can download and run this image using the following commands:

> docker pull adityajn105/deeplearning:latest
> docker run -d -p 8888:8888 -p 5000:5000 -e PASSWORD=password adityajn105/deeplearning:latest

Alternatively you can use mount bind in your host machine directoy (local directory) to access files.

> docker run -d -p 8888:8888 -p 5000:5000 -e PASSWORD=password -v $(pwd):/home/local adityajn105/deeplearning:latest 

*In Windows PowerShell, use ${PWD}*

## Contributors
* [Aditya Jain](https://adityajain.me)