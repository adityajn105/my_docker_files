FROM continuumio/miniconda3:4.8.2

RUN conda install -q -y flask=1.0.3 tensorflow=2.1.0

COPY app /home/app

WORKDIR /home/app

EXPOSE 80

CMD [ "python", "app.py" ]

