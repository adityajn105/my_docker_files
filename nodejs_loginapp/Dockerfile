FROM node:latest

WORKDIR /home

RUN wget -q https://github.com/cdr/code-server/releases/download/2.1698/code-server2.1698-vsc1.41.1-linux-x86_64.tar.gz \
  && tar -xvf code-server* \
  && mv code-server2.1698-vsc1.41.1-linux-x86_64 code-server \
  && rm -r *.tar.gz 

COPY my_app node

WORKDIR /home/node

RUN npm install

WORKDIR /home

ENV PASS aditya

VOLUME /home/node/profilephotos

COPY docker-entrypoint.sh .

EXPOSE 3000 5000

CMD ["bash","/home/docker-entrypoint.sh"]