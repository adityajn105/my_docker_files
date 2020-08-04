FROM continuumio/miniconda3:4.8.2

RUN conda install -q -y numpy=1.18.1 Pillow=5.4.1 opencv=3.4.2 \ 
	flask=1.0.3 grpcio=1.27.2 protobuf=3.11.4 && \
	conda clean --all

COPY app /home/app

ENV TF_SERVER_IP
ENV TF_SERVER_PORT

WORKDIR /home/app

EXPOSE 80

CMD [ "python", "app.py" ]