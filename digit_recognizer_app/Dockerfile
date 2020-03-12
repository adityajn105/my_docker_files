FROM continuumio/miniconda3:latest

RUN conda install -q -y opencv=3.4.2 flask=1.0.3 tensorflow=2.1.0

WORKDIR /home

COPY app .

VOLUME /home/app/stats

EXPOSE 80

RUN [ "python", "/home/app/app.py" ]

