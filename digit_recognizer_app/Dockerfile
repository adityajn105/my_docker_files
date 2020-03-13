FROM continuumio/miniconda3:latest

WORKDIR /home

RUN conda install -q -y opencv=3.4.2 flask=1.0.3 tensorflow=2.1.0

COPY app app

VOLUME /home/app/stats

EXPOSE 80

CMD [ "python", "/home/app/app.py" ]

