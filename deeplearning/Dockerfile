FROM tensorflow/tensorflow:latest-py3

RUN python -m pip install --quiet --no-cache-dir matplotlib flask pandas scikit-learn notebook

WORKDIR /home

RUN apt-get install wget \
    && wget -q https://github.com/cdr/code-server/releases/download/2.1698/code-server2.1698-vsc1.41.1-linux-x86_64.tar.gz \
    && tar -xvf *.tar.gz && rm *.tar.gz \
    && mv code-server* code-server

EXPOSE 8888 3000 5000

ENV PASSWORD aditya

COPY ./* /home/
CMD ["bash", "/home/docker-entrypoint.sh"]
