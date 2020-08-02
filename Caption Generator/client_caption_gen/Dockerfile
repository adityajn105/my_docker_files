FROM continuumio/miniconda3:4.8.2

RUN conda install -q -y opencv=3.4.2 flask=1.0.3 grpcio=1.27.2 protobuf=3.11.4 && \
	conda clean --all

COPY app /home/app

