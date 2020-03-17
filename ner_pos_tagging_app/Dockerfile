FROM continuumio/miniconda3:4.8.2

RUN conda install -q -y flask=1.0.3 tensorflow=2.1.0

WORKDIR /home

COPY app .

EXPOSE 80

RUN [ "python", "/home/app/app.py" ]